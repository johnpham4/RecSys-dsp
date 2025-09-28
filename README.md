# Data Prep with DBT and Feature Store

In this module we will explore conceptually how data is ETL from source systems into ML-specific data storeage.

We first push the interaction data into PostgreSQL to simulate transaction data.
Then we would create model using the dbt framework to extract and transform the source data into features used in ML model.
Finally we materialize the features from offline store into online store where it's stored in a Key-value manner which is optimized for inference use case.

# Prerequisite
- Poetry >= 1.8.3
- Miniconda or alternatives that can create new Python environment with a specified Python version
- Docker
- PostgreSQL
  - For Mac, run: `brew install postgresql`
  - For Ubuntu, run: `sudo apt-get update && sudo apt-get install -y gcc libpq-dev`

> [!IMPORTANT]
> **Increase Docker memory to 16GB**
> On MacOS, By default after installing Docker Desktop it might get only 8 GB of RAM from the host machine.
> Due to this project's poor optimization at the moment, it's required to increase the Docker allocatable memory to at least 14 GB.

# Set up
- Create a new `.env` file based on `.env.example` and populate the variables there
- Set up env var $ROOT_DIR: `export ROOT_DIR=$(pwd) && sed "s|^ROOT_DIR=.*|ROOT_DIR=$ROOT_DIR|" .env > .tmp && mv .tmp .env`
- Run `export $(grep -v '^#' .env | xargs)` to load the variables
- Create a new Python 3.11.9 environment: `conda create --prefix .venv python=3.11.9`
- Make sure Poetry use the new Python 3.11.9 environment: `poetry env use .venv/bin/python`
- Install Python dependencies with Poetry: `poetry install`

# Run the notebooks

```shell
# Start the Jupyter Lab service
make lab
```

Then you can go to to run the [notebook](./notebooks/001-start.ipynb)

# EDA
- Run this notebook [001-eda.ipynb](notebooks/001-eda.ipynb) to start explore our dataset.

# Simulate transaction data
- Run `cd $ROOT_DIR/data_prep && make up` to start PostgreSQL service
- Execute the notebook [002-simulate-oltp.ipynb](notebooks/002-simulate-oltp.ipynb) to populate the raw data into PostgreSQL

# Build feature table
```shell
cd $ROOT_DIR
cd data_prep/dbt/feast
# Specify credential for dbt to connect to PostgreSQL
cat <<EOF > profiles.yml
feast:
  outputs:
    dev:
      dbname: $POSTGRES_DB
      host: localhost
      pass: $POSTGRES_PASSWORD
      port: 5432
      schema: public
      threads: 1
      type: postgres
      user: $POSTGRES_USER
  target: dev
EOF
poetry run dbt build --models marts.amz_review_rating
```

# Test Feature Store
- Test feature store flow: `cd $ROOT_DIR/data_prep/fsds_feast/feature_repo && mkdir -p db && poetry run python test_workflow.py`

# Clean up

```shell
make clean
```