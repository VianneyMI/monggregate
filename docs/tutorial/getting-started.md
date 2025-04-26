# Getting Started with Monggregate

## Overview

Monggregate is a Python library designed to simplify working with MongoDB aggregation pipelines. It provides an object-oriented interface that lets you focus on data transformation requirements rather than MongoDB syntax.

## Installation

Monggregate is available on PyPI:

```shell
pip install monggregate
```

## Requirements

- Python 3.10 or higher
- Dependencies: `pydantic`, `pyhumps`, and `typing-extensions`
- A MongoDB driver for executing the query builder (e.g., `pymongo`)

For a complete list of requirements, see the [requirements files in the repository](https://github.com/VianneyMI/monggregate/blob/main/requirements).

## Basic Concepts

Monggregate's primary components:

- **Pipeline**: The main class used to build and chain MongoDB aggregation operations
- **Stages**: Individual operations like `match`, `group`, `sort`, etc.
- **Operators**: MongoDB operators implemented with intuitive Python syntax

## Quick Start Example

Here's a simple example to get you started:

```python
import pymongo
from monggregate import Pipeline

# Connect to MongoDB
client = pymongo.MongoClient("<insert-your-connection-string>")
db = client["sample_database"]

# Create a pipeline
pipeline = Pipeline()

# Build your pipeline with chained operations
pipeline.match(
    category="electronics"
).sort(
    by="price", 
    descending=True
).limit(5)

# Execute the pipeline
results = list(db["products"].aggregate(pipeline.export()))
print(results)
```

## Using the Pipeline Builder

The recommended way to use Monggregate is through the `Pipeline` class:

```python
from monggregate import Pipeline

# Initialize an empty pipeline
pipeline = Pipeline()

# Build your pipeline with autocomplete assistance
pipeline.match(...)
        .group(...)
        .sort(...)
```

When you type `pipeline.` in your IDE, you'll see all available aggregation stages through autocompletion:

![autocompletion](../img/demo_autocompletion.png)

## Advanced Usage

Monggregate supports advanced MongoDB features like expressions and operators:

```python
from monggregate import Pipeline, S

pipeline = Pipeline()
pipeline.match(
    year=S.type_("number")  # Using operators
).group(
    by="year",
    query={
        "count": S.sum(1),
        "titles": S.push("$title")
    }
)
```

## Next Steps

- Learn more about [building pipelines](pipeline.md)
- Explore available [aggregation stages](stages.md)
- Discover how to use [MongoDB operators](operators.md)
- Try [vector search capabilities](vector-search.md)