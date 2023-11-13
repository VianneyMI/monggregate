Operators are in a way the building blocks of stages.

## **Stages and Operators**

The relationship between operators and stages is similar to the relationship between stages and pipelines (but not exactly the same!).

The first main difference is that operators are optional for stages.<br>
For example, the `Match` stage can be used without any operator.

Conversely, some stages do not make a lot of sense if used without any operators.<br>
For example, the `Group` stage is not very useful by itself. It is meant to be used with operators to perform the actual aggregation.

Another difference is that operators are not necessarily used sequantially, they can also be used in parallel.<br>
For example, the `Group` stage can be used with the `$sum` and `$push` operators at the same time, depending on the requirements.

## **Compatibility**

Some operators are not meant to be used with some stages. Others behave differently depending on the stage they are used in.
Those compatibility rules are detailed in the documentation of each operator as monggregate documentation integrates a good part of the MongoDB documentation.<br>
<should I remove the code syntaxing for mergeObjects ? or add it for the below stage -- Need to be consistent across the doc>
For example the `$mergeObjects` operator documentation clearly states that it can only be used in the following stages:

* `$bucket`
* `$bucketAuto`
* `$group`
* `$replaceRoot`


## **Usage**

Because of the above considerations, the usage of operators is a bit different than the usage of stages.

You cannot access the operators through the stages, the same way you can access the stages through the pipeline (eventhough it's on our development roadmap).

Therefore, you need to import the operators from the `monggregate.operators` namespace.
Or you can use the `S` shortcut to access the operators.<br>
`S` is an object that includes all the operators as functions, like the `Pipeline` class includes all the stages as methods.
<insert link to documentation>

Thus, the grouping example would become:

```python
pipeline = Pipeline()

pipeline.group(
    by="year",
    query={
        "movie_count": S.sum(1),
        "movie_titles": S.push(S.field("title"))
    }
)

```
## **List of Available Operators In Monggregate**

Currently, monggregate supports the following operators:

* **Accumulators**

    * `$avg`
    * `$count`
    * `$first`
    * `$last`
    * `$max`
    * `$min`
    * `$push`
    * `$sum`

* **Arithmetic**

    * `$add`
    * `$divide`
    * `$multiply`
    * `$pow`
    * `$subtract`

* **Array**

    * `$arrayToObject`
    * `$filter`
    * `$first`
    * `$in`
    * `$isArray`
    * `$last`
    * `$max_n`
    * `$min_n`
    * `$size`
    * `$sortArray`

* **Boolean**

    * `$and`
    * `$not`
    * `$or`

* **Comparison**

    * `$cmp`
    * `$eq`
    * `$gt`
    * `$gte`
    * `$lt`
    * `$lte`
    * `$ne`
    
* **Conditional**

    * `$cond`
    * `$ifNull`
    * `$switch`

* **Date**

    * `$millisecond`

* **Object**

    * `$mergeObjects`
    * `$objectToArray`

* **Strings**

    * `$concat`
    * `$dateFromString`
    * `$dateToString`

* **Search**

    * See [search page](search.md)


## **Disambiguation**

Some operators have MQL homonyms (i.e. operators with the same name in MongoDB Query Language), that have a slightly different syntax or usage.

`$gte` is an example of such operator.<br>
Its syntax is not the same in an aggregation pipeline than in a MQL query.

In a MQL query, you are going to use it as follows:

```python
{
    "year": {"$gte": 2010}
}
```

In an aggregation pipeline, you are going to use it as follows:

```python
{
    "$gte": ["$year", 2010]
}
```

In other cases, there are aggregation operators that can be used as-is in MQL queries.
<add examples>