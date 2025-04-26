# **MongoDB Aggregation Pipelines**

Pipelines are a fundamental concept in MongoDB's aggregation framework, providing a powerful way to process and transform data. The `Pipeline` class in Monggregate is designed to make building and executing these pipelines intuitive and efficient.

## **Building a Pipeline**

The `Pipeline` class is the core of Monggregate, offering methods that correspond to each MongoDB aggregation stage. Every stage in MongoDB's aggregation framework has an equivalent class and method in Monggregate.

### **Basic Pipeline Construction**

Creating a pipeline is straightforward:

```python
from monggregate import Pipeline

# Initialize an empty pipeline
pipeline = Pipeline()

# Add a Match stage to filter documents
pipeline.match(title="A Star Is Born")
```

Each method returns the pipeline instance, enabling method chaining to build complex pipelines with a clean, readable syntax:

```python
from monggregate import Pipeline

# Build a multi-stage pipeline
pipeline = Pipeline()
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year",
    descending=True
).limit(
    value=1
)
```

This pipeline will filter for movies titled "A Star Is Born", sort them by year in descending order, and return only the first result (the most recent movie with that title).

## **Executing a Pipeline**

Monggregate provides a simple way to export your pipeline to a format compatible with your MongoDB driver or ODM of choice:

```python
import pymongo
from monggregate import Pipeline

# Connect to MongoDB
MONGODB_URI = "<insert-your-connection-string>"
client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"]

# Create and build your pipeline
pipeline = Pipeline()
pipeline.match(
    title="A Star Is Born"
).sort(
    by="year"
).limit(
    value=1
)

# Execute the pipeline
cursor = db["movies"].aggregate(pipeline.export())
results = list(cursor)
print(results)
```

The `export()` method converts your Monggregate pipeline into the standard MongoDB format (a list of stage dictionaries) that any MongoDB driver can execute.

## **Alternative: Using Stage Classes Directly**

For more complex scenarios or when you need to reuse stages, you can work directly with stage classes:

```python
import pymongo
from monggregate import Pipeline, stages

# Connect to MongoDB
MONGODB_URI = "mongodb://localhost:27017"
client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"]

# Create individual stage instances
match_stage = stages.Match(query={"title": "A Star Is Born"})
sort_stage = stages.Sort(by="year")
limit_stage = stages.Limit(value=1)

# Combine stages into a pipeline
pipeline_stages = [match_stage, sort_stage, limit_stage]
pipeline = Pipeline(stages=pipeline_stages)

# Execute the pipeline
cursor = db["movies"].aggregate(pipeline.export())
results = list(cursor)
print(results)
```

This approach offers advantages:
- Stages can be reused across multiple pipelines
- Stages can be easily reordered or modified
- Complex stage configurations can be built separately

## **Complex Example: Analysis Pipeline**

Here's a more comprehensive example that analyzes movies by genre:

```python
import pymongo
from monggregate import Pipeline, S

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["sample_mflix"]

# Build an analysis pipeline
pipeline = Pipeline()
pipeline.match(
    year={"$gte": 2000}  # Movies from 2000 onwards
).unwind(
    path="genres"  # Split documents by genre
).group(
    by="genres",  # Group by genre
    query={
        "count": S.sum(1),  # Count movies per genre
        "avg_imdb": S.avg("$imdb.rating"),  # Average IMDB rating
        "titles": S.push("$title")  # Collect titles
    }
).match(
    count=S.gt(10)  # Only include genres with >10 movies
).sort(
    by="avg_imdb",
    descending=True
)

# Execute the pipeline
results = list(db["movies"].aggregate(pipeline.export()))
for genre in results:
    print(f"{genre['_id']}: {genre['count']} movies, {genre['avg_imdb']:.2f} avg rating")
```

## **Pipeline Manipulation**

The `Pipeline` class implements Python's list interface, allowing you to manipulate stages programmatically:

```python
# Check pipeline length
print(len(pipeline))  # Returns number of stages

# Add a stage to the end
pipeline.append(stages.Project(title=1, year=1))

# Add multiple stages
pipeline.extend([
    stages.Skip(10),
    stages.Limit(5)
])

# Insert a stage at a specific position
pipeline.insert(0, stages.Match(year=2020))
```

This makes pipelines highly flexible and enables dynamic pipeline construction based on conditions or user input.

## **Next Steps**

- Learn about available [aggregation stages](stages.md)
- Explore [MongoDB operators](operators.md) for advanced data manipulation
- Discover [vector search capabilities](vector-search.md) for similarity queries
