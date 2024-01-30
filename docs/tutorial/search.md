The aggregation framework provide advanced search functionalities through the `$search` and `$searchMeta` stages.

Note: the `$search` and `$searchMeta` stages are only available with MongoDB Atlas.

## **Atlas Search**

Atlas Search offers similar features than other search engines like ElasticSearch or Algolia.
Such features include:

- Full-text search
- Fuzzy search
- Autocompletion
- Highlighting
- Faceting
- Geospatial search
- Relevance scoring
- Query analytics

You can see a more detailled list of features [here](https://www.mongodb.com/docs/atlas/atlas-search/atlas-search-overview/).

## **Using Atlas Search through monggregate**

Like for the other stages `monggregate` defines a class and a `pipeline` method for the search stages.
However, there is a slight difference with the other stages. The search stages are themselves very similar to pipelines.
You will better grasp this concept in one [the below sections](#search-pipelines).

The search stages define their own set of operators called **search operators**.
Below an non-exhaustive list of the search operators:

* Autocomplete
* Compound
* Text
* Regex 

Like for the other stages the search stages can be enhanced with one or several operators. Unlike the other stages, it is required to use at least one operator with the search stages.
The operators listed previously are some of most commonly used operators. 

The `text` operator is the central operator that allows to perform full-text search. It takes in an optional fuzzy parameter which allows to perform fuzzy search.

The `autocomplete` operator allows to perform autocompletion. 

The `compound` operator allows to combine several search operators together while giving each of them a different weight or role thanks to the clause types `filter`, `must`, `mustNot` and `should`. 

* `filter` clauses define text that must be present in the documents matching the query.
* `must` clauses are similar to `filter` clauses, but they also affect the relevance score of the documents.
* `mustNot` clauses define text that must not be present in the documents matching the query.
* `should` clauses define text that may be present in the documents matching the query. They also affect the relevance score of the documents. A minimum number of `should` clauses matches can be defined through the `minimumShouldMatch` parameter.

The `facet` collector (sort of operator) allows to perform faceting on the results of the search. It is a very powerful feature and common feature in good search experiences.

Again, the search features are so vast, that they could have their own package, but fortunately for you, they have been included in `monggregate`.

How do you build search queries with `monggregate`? Let's see that in the next section.
In the next sections, we will only talk about the `$search` stage, but everything applies to the `$searchMeta` stage as well.

## **Basic Search**

The `Search` class the and the `search` method have default parameters so that it is easy to quickly get started. 

Building your search request is as simple as, the following code:

```python

pipeline.search(
        path="description"
        query="apple", 
    )

```

By default, the search will be performed on the `text` operator.

You can also enhance your the search experience by making a fuzzy search, just by adding the `fuzzy` parameter:


```python

from monggregate.search.commons import FuzzyOptions

pipeline.search(
        path="description"
        query="apple", 
        fuzzy=FuzzyOptions(
            max_edits=2
        )
    )

```

You can build even richer search queries by adding more operators to your search stage as shown in the next section.

## **Search Pipelines**


The search stages can be composed of multiple search operators, thus defining a compound search.
As such, unlike for other stages, calling the `search` method on a `pipeline` object several times will not add a new `search` stage every time. Instead, every call will complete the previous `search` stage by appending a new clause or a new facet.

NOTE: The `$search` stage has to be the first stage of the pipeline.

As an example, the following code:
```python
pipeline.search(
        index="fruits", 
        operator_name="compound"
    ).search( 
        clause_type="must", 
        query="varieties", 
        path="description"
    ).search(
        clause_type="mustNot",
        query="apples",
        path="description"
    )
```
will generate the following pipeline:
```json
[
    {
        "$search": {
            "index": "fruits",
            "compound": {
                "must": {
                    "query": "varieties",
                    "path": "description"
                },
                "mustNot": {
                    "query": "apples",
                    "path": "description"
                }
            }
        }
    }
]
```

This example was copied from a past version* of MongoDB official doc and has just been adapted to `monggregate` syntax.
Let's review what is going on here.

The first search call, initializes a `$search` stage with an "empty" `compound` operator.
The second search call, completes the `compound` operator by adding a `text` operator in a `must` clause.
The third search call, appends a `text` operator in a `mustNot` clause to the `compound` operator.

At the end, the generated query will return documents containing the word "varieties" in the "description" field, but not containing the word "apples" in the "description" field.

*Unfortunately, the current version of the doc does not provide such example anymore. It is planned that we update this page to use the movies collection instead.

## **Faceted Search**

Unlike previous sections, this section will be illustrated with the `search_meta` method instead of the `search` method, as it is a bit more relevant in the context of faceted search.

`monggregate` eases the process of building faceted search queries.

You can initialize a faceted search query as follows:

```python
pipeline = Pipeline()
pipeline.search_meta(
    index="fruits",
    collector_name="facet",

)
```

Then, you can add facets to your search query as follows:

```python
pipeline.search_meta(
    facet_type="string",
    path="category",
)
```

The first code sample initializes the faceted search but it is not usable as such. It is required to add at least one facet to the search query.

The second code sample adds a facet to the search query. The facet is of type `string` and will be performed on the `category` field.

After initializing the faceted search, you can add as many facets as you want to your search query and you can also add other search operators to your search query (in the order that you want) such that the facets will be performed on the results of the search.
