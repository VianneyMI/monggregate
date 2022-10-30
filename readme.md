## Overview

Monggregate is a library that aims at simplifying usage of MongoDB aggregation pipeline in python.
It is based on MongoDB official python driver, pymongo and on [pydantic](https://pydantic-docs.helpmanual.io/).

### Features

Monggregate:

    * provides an OOP interface to the aggregation pipeline and allows you to not having to remember all the syntatical details of the aggregation framework.
    * integrates all the MongoDB documentation and allows you to quickly refer to it without having to navigate to the website.
    * offers a pandas-style way to chain operations on data.


## Installation

1. Download the repo from https://github.com/VianneyMI/mongreggate
2. Copy the repo to your project
3. Navigate to the folder containing the dowloaded repo
4. Install the repo locally by executing the following command: ` python -m pip install -e .`

## Usage

The below examples reference the  MongoDB sample_mflix database

### ... through the stage classes

```python

from dotenv import load_dotenv
import pymongo
from monggregate.app.stages import Match, Limit Sort

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

### ... through the pipeline inteface

#### Approach #1

```python

from dotenv import load_dotenv
import pymongo
from monggregate.app.pipeline import Pipeline

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Creating the pipeline
pipeline = Pipeline(
    collection="movies",
)

pipeline.match(
    query = {
        "title" : "A Star is Born"
    }
).sort(
    query = {
        "year":1
    }
).limit(
    value=1
)

# Executing the pipeline
db["movies"].aggregate(pipeline())

```

#### Approach #2

```python

from dotenv import load_dotenv
import pymongo
from monggregate.app.pipeline import Pipeline

# Load config from a .env file:
load_dotenv(verbose=True)
MONGODB_URI = os.environ["MONGODB_URI"]

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Creating the pipeline
pipeline = Pipeline(
    _db=db,
    on_call="run",
    collection="movies",
)

pipeline.match(
    query = {
        "title" : "A Star is Born"
    }
).sort(
    query = {
        "year":1
    }
).limit(
    value=1
)

# Executing the pipeline
pipeline()
