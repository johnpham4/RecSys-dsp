.PHONY:
.ONESHELL:

include .env
export

lab:
	poetry run jupyter lab --port 8888 --host 0.0.0.0

