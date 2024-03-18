MongoDB has developed one of the most complete database management systems in the market.

Although it is mainly known for being a document-oriented NoSQL database with optional schemas. It has evolved and expanded to offer a wide range of features and services around data management. 

However, here we will focus on the database itself and in particular its query languages.

## **MQL**

**MQL** stands for **M**ongoDB **Q**uery **L**anguage. It is the language used to query MongoDB databases. It is a JSON-based query language that allows you to query documents in a collection.

**MQL** allows you to [perform CRUD operations](https://www.mongodb.com/docs/manual/crud/), that inserts (**C**reate), queries (**R**ead), updates (**U**pdate) and deletes (**D**elete) documents in a collection.

In the context of an application or web service, **MQL** would typically be used through a driver or an Object Document Mapper (ODM).<br>
The official MongoDB driver for Python is [PyMongo](https://pymongo.readthedocs.io/en/stable/). It is a low-level driver that allows you to interact with MongoDB databases. And two of the most popular ODM are [MongoEngine](https://mongoengine-odm.readthedocs.io/) and [Beanie](https://beanie-odm.dev/).

**MQL** is not the main topic of monggregate nor this documentation, which is about the aggregation framework.

## **Aggregation Framework**

[Quickly after the release of MongoDB, the MongoDB team realized that the query language was not sufficient to perform complex queries](https://www.practical-mongodb-aggregations.com/intro/history.html).

In particular, there was a gap to do analytics on the data like it is easily done in SQL. 

Hence the release of [Aggregation Framework](https://docs.mongodb.com/manual/aggregation/) later on. 

As I stated in [my article](https://medium.com/dev-genius/mongo-db-aggregations-pipelines-made-easy-with-monggregate-680b322167d2)
> Aggregation pipelines are the tool that allow MongoDB databases to really rival their SQL counterparts.

The pymongo driver nor the ODMs mentioned above offer a way to easily use the aggregation framework. They only let you do your aggregation queries as raw strings.

This is where `monggregate` comes in.
`monggregate` exposes an Object Oriented Programming (OOP) interface to the aggregation framework that make it easier to build pipelines.

In the [following page](mongodb-aggregation-framework.md), we will do a deep-dive on the aggregation framework.

## **Atlas Search**

[Atlas Search ](https://www.mongodb.com/docs/atlas/atlas-search/atlas-search-overview/) is a full-text search service that is fully integrated with MongoDB Atlas. It allows you to perform text search on your data and is based on [Apache Lucene](https://lucene.apache.org/).

As the aggregation framework is the entry point for Atlas Search, `monggregate` also offers a way to use it.
Check out the search page[here](../tutorial/search.md) for more details.

## **MongoDB Latest Features**

MongoDB also offers capabilities for **time series** collections, semantic and **vector search** and probably much more that may or may not be integrated in monggregate in the future.

But, as of today, these features are not in the scope of `monggregate`.
