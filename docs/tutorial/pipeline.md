
Pipelines are a key concept in the aggregation framework.
Therefore, the  `Pipeline` class is also a central class in the package<include link to api reference later on>, as it is used to build and execute pipelines.

## **Building a pipeline**

<include link to api reference later on>
The `Pipeline` class includes a method for each stage of the aggregation framework.<br>
Each stage of the aggregation framework also has its own class in the package.
And each `Stage` class has a mirror method in the `Pipeline`.

For example, the `Match` stage has a `match` method in the `Pipeline` class and calling `pipeline.match()` like in the code snippet below.

```python
from monggregate import Pipeline

pipeline = Pipeline()

pipeline.match(title="A Star Is Born")
```

will add a `Match` stage instance to the pipeline and return the pipeline instance.

That way, you can chain the stages together to build your pipeline.

```python
from monggregate import Pipeline

pipeline = Pipeline()

# The below pipeline will return (when executed) 
# the most recent movie with the title "A Star is Born"
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year"
).limit(
    value=1
)
```	

## **Executing a pipeline**

So far, we have built our pipeline object. But what do we do with it?

monggregate offers a **bilateral** integration with your tool of choice to execute the pipeline.

Bilateral because you can either integrate your pipeline to your tool or your tool to your pipeline.
In the following examples, I'll use `pymongo` as at the end of the day `motor`, `beanie` and `mongoengine` all use pymongo under the hood.

### **Passing your pipeline to your tool**

The `Pipeline` class has an `export` method that returns a list of dictionaries of raw MongoDB aggregation language, which is the format expected by `pymongo`.

```python

import pymongo
from monggregate import Pipeline, S

# Setup your pymongo connexion
MONGODB_URI = f"insert_your_own_uri"
client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"]

# Create your pipeline
pipeline = Pipeline()

# Build your pipeline
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year"
).limit(
    value=1
)

# Execute your pipeline
curosr = db["movies"].aggregate(pipeline.export())

results = list(curosr)
print(results)
```
### **Passing your tool to your pipeline**

The pipeline class also has `run` method, a `_db` and a `collection` attributes that you can set that make your pipelines callable and runnable by being aware of your database connexion.<br>
Thus, you could write the above example like this:

```python
import pymongo
from monggregate import Pipeline, S

# Setup your pymongo connexion
MONGODB_URI = f"insert_your_own_uri"
client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"]

# Create your database aware pipeline
pipeline = Pipeline(_db=db, collection="movies") 

# Build your pipeline
# (This does not change)
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year"
).limit(
    value=1
)

# Execute your pipeline
# (The execution is simpler)
results = pipeline.run()
print(results)
```

It also has a `__call__` method, so you could  replace the two last lines with:

```python
results = pipeline()
print(results)
```

### **Pros and cons of each method**