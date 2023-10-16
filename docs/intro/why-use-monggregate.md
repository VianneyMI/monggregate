In this page, we will present the various reasons one may want to use monggregate.

## **What monggregate is ?**

As a disclaimer, I'll start by saying what monggregate is not.

Monggregate **IS NOT** a MongoDB driver **NOR** an Object Document Mapper (ODM).

Monggregate can be seen as a NoSQL **query builder** for MongoDB.

If you are not familiar with the concept of query builder, I suggest you watch [this video](https://www.youtube.com/watch?v=x1fCJ7sUXCM) from Arjan Codes where he explains the difference between using raw SQL, query builders and ORMs.
Even if the examples use SQL, there are still relevant in a NoSQL context.

## **Why use monggregate ?**

With that said, when or why would one want to use monggregate ?
As written in the [previous page](mongodb-aggregation-framework.md), the aggregation framework can be used for data analytics, data transformation and much more.

However, it is not convenient to use with the available tools overall and in python in particular (even if MongoDB as recently [2023] tried to overcome this by releasing several helpers such as the stage wizard and a chat assistant to help building queries).

The main critiques that we can have about the aggregation framework either about the framework itself or about its accesibility in python are the following:

* It has a steep learning curve
* It is quite verbose
* There is no python API to use it
* It is undocumented in pymongo

Monggregate tries to solve these issues by providing a python API to use the aggregation framework.

The API improves the readability of the pipelines and make the queries less verbose.

It also integrates most of the official MongoDB documentation available directly in the code. Therefore, you no longer have to navigate between the documentation and your code. You no longer have to try your pipelines on Compass or Atlas to see if they work. You can do it directly in your application code. You could for example, try out your pipelines in a test suite or in a notebook.

Cherry on the cake, your IDE will help you in the process because you now have autocompletion showing you the available stages and operators, their parameters, types, descriptions and restrictions.

## **How to use it ?**

In the following section, we will see how to use monggregate to build aggregation pipelines.
