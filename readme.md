## **Overview**

Monggregate is a library that aims at simplifying usage of MongoDB aggregation pipelines in Python.
It is based on MongoDB official Python driver, pymongo and on [pydantic](https://pydantic-docs.helpmanual.io/).

### Features

- Provides an Object Oriented Programming (OOP) interface to the aggregation pipeline.
- Allows you to focus on your requirements rather than MongoDB syntax.
- Integrates all the MongoDB documentation and allows you to quickly refer to it without having to navigate to the website.
- Enables autocompletion on the various MongoDB features.
- Offers a pandas-style way to chain operations on data.

## **Requirements**

This package requires python > 3.10, pydantic > 1.8.0

## **Installation**

The repo is now available on PyPI:

```shell
pip install monggregate
```


## **Usage**

The below examples reference the MongoDB sample_mflix database

### Basic Pipeline usage

```python
import os

from dotenv import load_dotenv 
import pymongo
from monggregate import Pipeline, S

# Creating connexion string securely
# You need to create a .env file with your password
load_dotenv(verbose=True)
PWD = os.environ["MONGODB_PASSWORD"] 

MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"

# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Creating the pipeline
pipeline = Pipeline()

# The below pipeline will return the most recent movie with the title "A Star is Born"
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year"
).limit(
    value=1
)

# Executing the pipeline
curosr = db["movies"].aggregate(pipeline.export())

# Printing the results
results = list(curosr)
print(results)
```



### Advanced Usage, with MongoDB Operators


```python
import os

from dotenv import load_dotenv 
import pymongo
from monggregate import Pipeline, S


# Creating connexion string securely
load_dotenv(verbose=True)
PWD = os.environ["MONGODB_PASSWORD"]
MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"


# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]


# Creating the pipeline
pipeline = Pipeline()
pipeline.match(
    year=S.type_("number") # Filtering out documents where the year field is not a number
).group(
    by="year",
    query = {
        "movie_count":S.sum(1), # Aggregating the movies per year
        "movie_titles":S.push("$title")
    }
).sort(
    by="_id",
    descending=True
).limit(10)

# Executing the pipeline
cursor = db["movies"].aggregate(pipeline.export())

# Printing the results
results = list(cursor)
print(results)

```

### Even More Advanced Usage with Expressions

```python
import os

from dotenv import load_dotenv 
import pymongo
from monggregate import Pipeline, S, Expression

# Creating connexion string securely
load_dotenv(verbose=True)
PWD = os.environ["MONGODB_PASSWORD"]
MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"


# Connect to your MongoDB cluster:
client = pymongo.MongoClient(MONGODB_URI)

# Get a reference to the "sample_mflix" database:
db = client["sample_mflix"]

# Using expressions
comments_count = Expression.field("comments").size()


# Creating the pipeline
pipeline = Pipeline()
pipeline.lookup(
    right="comments",
    right_on="movie_id",
    left_on="_id",
    name="comments"
).add_fields(
    comments_count=comments_count
).match(
    expression=comments_count>2
).limit(1)

# Executing the pipeline
cursor = db["movies"].aggregate(pipeline.export())

# Printing the results
results = list(cursor)
print(results)
```

## **Going Further**

* Check out the [full documentation](https://vianneymi.github.io/monggregate/) for more examples.
* Check out this [medium article](https://medium.com/@vianney.mixtur_39698/mongo-db-aggregations-pipelines-made-easy-with-monggregate-680b322167d2).
