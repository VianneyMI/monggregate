
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

### **How to choose ?**

It is up to you to choose the method that suits you the best.<br> 
The author recommends the first method as monggregate is a relatively new package and the second method is still experimental.

## **An alternative to build pipelines**

Another way to build your pipeline is to access the stages classes directly. All the stages are accessible in the `monggregate.stages` namespace.
As such, you could write the above example like this:

```python

import pymongo
from monggregate import Pipeline, stages


# Setup your pymongo connexion
MONGODB_URI = f"insert_your_own_uri"
client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"]

# Prepare your stages
match_stage = stages.Match(query={"title": "A Star Is Born"})
sort_stage = stages.Sort(by="year")
limit_stage = stages.Limit(value=1)
stages = [match_stage, sort_stage, limit_stage]

# Create your pipeline ready to be executed
pipeline = Pipeline(stages=stages)

# Execute your pipeline
curosr = db["movies"].aggregate(pipeline.export())

results = list(curosr)
print(results)

```
Once again, it is a question of preferences.<br>
This approach might be more readable for some people, but it is also more verbose.<br>

Howevere, there are still a couple of other advantages with this approach:

* You can reuse the stages in multiple pipelines
* You can easily reorder the stages

The second point is particularly relevant given the utilies function in the `Pipeline` class.

## **Pipeline utilities**

The `Pipeline` class has a few utilities methods to help you build your pipeline.

Indeed it implements the python list methods, so you do not have to access the stages attribute to perform list operations.

In the examples above, `len(pipeline)` would return 3.

You could also for example append a stage to the pipeline like this:

```python
pipeline.append(stages.Project(title=1, year=1))
```

You also have access to the `append`, `extend`, `insert`, `pop`, `remove`, `reverse`, `sort` methods. <TODO: implement pop remove and reverse>
