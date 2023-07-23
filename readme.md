## Overview

Monggregate is a library that aims at simplifying usage of MongoDB aggregation pipelines in python.
It is based on MongoDB official python driver, pymongo and on [pydantic](https://pydantic-docs.helpmanual.io/).

### Features


- provides an OOP interface to the aggregation pipeline.
- allows you to focus on your requirements rather than MongoDB syntax
- integrates all the MongoDB documentation and allows you to quickly refer to it without having to navigate to the website.
- enables autocompletion on the various MongoDB features.
- offers a pandas-style way to chain operations on data.

## Requirements

This package requires python > 3.10, pydantic > 1.8.0

## Installation

### PIP

The repo is now available on PyPI:

```shell
pip install monggregate
```

### Manually

1. Download the repo from https://github.com/VianneyMI/mongreggate
2. Copy the repo to your project
3. Navigate to the folder containing the downloaded repo
4. Install the repo locally by executing the following command: ` python -m pip install -e .`

## Usage

The below examples reference the MongoDB sample_mflix database

### ... through the pipeline interface

```python

from dotenv import load_dotenv
import pymongo
from monggregate.pipeline import Pipeline

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Creating the pipeline
pipeline = Pipeline()

pipeline.match(
    title="A Star is Born"
).sort(
    value="year"
).limit(
    value=1
)

# Executing the pipeline
db["movies"].aggregate(pipeline.export())

```


### ... through the stage classes

```python

from dotenv import load_dotenv
import pymongo
from monggregate.stages import Match, Limit Sort

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Get a reference to the "movies" collection:
movie_collection = db["movies"]

# Creating the pipeline
filter_on_title = Match(
    query = {
        "title" : "A Star is Born"
    }
)
sorting_per_year = Sort(
    query = {
        "year":1
    }
)

limiting_to_most_recent = Limit(
    value=1
)

pipeline = [filter_on_title, sorting_per_year, limiting_to_most_recent]
pipeline = [stage.statment for stage in pipeline]

# Lauching the pipeline

results = move_collection.aggregate(pipeline)

```


## Motivation

The main driver for building this package was how unconvenient it was for me to build aggregation pipelines using pymongo or any other tool.

With pymongo, which is the official MongoDB driver for python, there is no direct support for aggregation pipelines.

pymongo exposes an `aggregate` method but the pipeline inside is just a list of complex dictionaries that quickly become quite long, nested and overwhelming.

At the end, it is barely readable for the one who built the pipeline. Let alone other developers.
Besides, during the development process, it is often necessary to refer to the online documentation multiple times. Thus, the package aims at integrating the online documentation through in the docstrings of the various classes and modules of the package.
Basically, the package mirrors every* stage and operator available on MongoDB.

*Actually, it only covers a subset of the stages and operators available. Please come help me to increase the coverage. 

## Roadmap

As of now, the package covers 50% of the available stages and 20% of the available operators.
The goal is to quickly reach 100% of both stages and operators.
The source code integrates most of the online MongoDB documentation. If the online documentation evolves, it will need to be updated here as well.
The current documentation is not consistent throughout the package it will need to be standardized later on.
Some minor refactoring tasks are required also.

There are already a couple issue, that I noted myself for the next tasks that are going to be tackled.

Feel free to open an issue, if you found a bug or to propose enhancements.
Feel free to do a PR, to propose new interfaces for stages that have not been dealt with yet.

## Going further

* Check out this GitHub [repo](https://github.com/VianneyMI/doc_monggregate) for more examples.
* Check out this [tutorial](https://medium.com/@vianney.mixtur_39698/mongo-db-aggregations-pipelines-made-easy-with-monggregate-680b322167d2) on Medium. (It's not under the paywall)
