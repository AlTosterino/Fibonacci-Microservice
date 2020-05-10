[![Build Status](https://travis-ci.com/AlTosterino/Fibonacci-Microservice.svg?branch=master)](https://travis-ci.com/AlTosterino/Fibonacci-Microservice)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Fibonacci microservice
Generating and populating database with consecutive numbers of Fibonacci sequence.
Generator is generating values from start (or if numbers already in database, then values will start at the last saved number) and sending them to RabbitMQ queue. 
Then Consumer will consume numbers and save them to SQL database.
API is responsible for showing generated numbers.

## Prerequisites
1. [Python 3.7/3.8](https://www.python.org/downloads/)
2. [Pipenv](https://github.com/pypa/pipenv) for easier install via virtual environment.
3. [RabbitMQ](https://www.rabbitmq.com/)
4. SQL Database

## Installing
1. **CLONE** this repository - This is very important step
2. Run `python setup.py install` inside project root, or if You want to use pipenv -> `pipenv install` then `pipenv shell` and the last `python setup.py install`
3. Now You will have three commands available on Your system (or in virtual environment if used pipenv) 

## Configuring
To configure script copy `example_config.yaml` and populate it with desired values.

## Using

### Consumer
> Note: You need to have database and message queue running before using Consumer

Use `fib_consumer -c config_file.yaml` command to invoke script.

### Generator
> Note: You need to have database and message queue running before using Generator

Use `fib_generator -c config_file.yaml` command to invoke script.

### API
> Note: You need to have database and message queue running before using API

Use `fib_api -c config_file.yaml` command to invoke script.

## Running with docker 
Simply invoke command: `docker compose up -d`
Now, the API will be available on: `localhost:8000`
> You can also modify script settings inside docker, changing values in docker_config.yaml

## Testing
To test the script use `python setup.py test` command.
  
  ---

This project has been set up using PyScaffold 3.2.3. For details and usage information on PyScaffold see https://pyscaffold.org/.