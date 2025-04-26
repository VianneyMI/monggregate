# 🔄 **MongoDB Aggregation Stages**

**Stages** are the building blocks of aggregation pipelines.

> 📘 We saw in the [previous page](pipeline.md) two methods to compose stages to effectively build a pipeline:
>
> * Using the pipeline stages methods
> * Using the stages classes directly

Repeating what was described previously:

> 💡 Each stage of the aggregation framework also has its own class in the package.
> And each `Stage` class has a mirror method in the `Pipeline`.

There is actually an asterisk to this. Monggregate does not yet provide an interface to all of the stages provided by MongoDB.
It is a work in progress and the list of available stages will grow over time. If you want to contribute, please refer to the [contributing guide](../contributing.md).

You can see the full list of stages provided by MongoDB [here](https://www.mongodb.com/docs/manual/reference/aggregation-quick-reference/#stages--db.collection.aggregate-).

## 📋 **List of Available Stages In Monggregate**

The following table lists the stages that are currently available in Monggregate:

* `$addFields`
* `$bucket`
* `$bucketAuto`
* `$count`
* `$group`
* `$limit`
* `$lookup`
* `$match`
* `$merge`
* `$out`
* `$project`
* `$replaceRoot`
* `$replaceWith`
* `$sample`
* `$search`
* `$searchMeta`
* `$set`
* `$skip`
* `$sort`
* `$sortByCount`
* `$unionWith`
* `$unset`
* `$unwind`

## 🚀 **Usage**

> 🎯 `monggregate` aims at providing a simple and intuitive interface to the MongoDB aggregation framework.

Even though, it tries as much as possible to stick by the MongoDB aggregation framework syntax, it also tries to provide alternative ways to reproduce the syntax of other tools that new Mongo users might be more familiar with such as SQL and Pandas.

For example, in the `$group` stage, the MongoDB aggregation framework expects the grouping field(s) to be provided in the `_id` key. However, `monggregate` allows you to provide the grouping field(s) in the `by` key instead.

```python
pipeline = Pipeline()

pipeline.group(
    by="year",
    query={
        "movie_count": {"$sum": 1},
        "movie_titles": {"$push": "$title"}
    }
)
```

Similarly, `monggregate` pipeline `lookup` method and `Lookup` class provide aliases for the orignal MongoDB arguments:

| MongoDB Original Name | Monggregate Original Name | Monggregate Convenient Alias |
|-----------------------|---------------------------|------------------------------|
| from                  | from                      | right                        |
| localField            | local_field               | left_on                      |
| foreignField          | foreign_field             | right_on                     |
| as                    | as                        | name                         |

> ℹ️ **Note**: The original names of the arguments were converted to snake_case to follow the Python convention.
> You cannot use the camelCase version of the arguments names here.

You can therefore use any combination of arguments names from the two rightmost columns above to build your stage.

```python
pipeline = Pipeline()
pipeline.lookup(
    right = "comments", # collection to join
    left_on = "_id",  # primary key
    right_on = "movie_id", # foreign key
    # name of the field that will contain the matching documents
    name = "related_comments" 
)
```

When using the stages methods, you can sometimes omit to name the argument(s).
We can for example complete the previous example as follows:

```python
pipeline = Pipeline()
pipeline.lookup(
    right = "comments", 
    left_on = "_id", 
    right_on = "movie_id",
    name = "related_comments" 
).sort(
    "movie_count"
).limit(
    10
)
```
> 🔍 The arguments names (`by` and `value` respectively) for the `sort` and `limit` stages are omitted.

## 🛠️ **Operators**

You might have noticed in the grouping example how we tell Monggregate to perform operations on the groups.
In the example, we used the `$sum` and `$push` operators.

> 🔜 For more information about operators, check the [next page](operators.md).
