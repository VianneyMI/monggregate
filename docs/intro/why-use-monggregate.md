In this page, we will present the various reasons one may want to use `monggregate`.

## **What is Monggregate?**

As a disclaimer, I'll start by saying what `monggregate` is not.

`monggregate` **IS NOT** a MongoDB driver **NOR** an Object Document Mapper (ODM).

`monggregate` can be seen as a NoSQL **query builder** for MongoDB.

If you are not familiar with the concept of query builder, I suggest you watch [this video](https://www.youtube.com/watch?v=x1fCJ7sUXCM) from Arjan Codes where he explains the difference between using raw SQL, query builders and Object–relational mappings (ORMs).
Even if the examples use SQL, there are still relevant in a NoSQL context.

## **Why Use Monggregate ?**

With that said, when or why would one want to use `monggregate` ?
As written in the [previous page](mongodb-aggregation-framework.md), the aggregation framework can be used for data analytics, data transformation and much more.

However, it is not convenient to use with the available tools overall and in Python in particular (even if MongoDB as recently [2023] tried to overcome this by releasing several helpers such as the stage wizard and a chat assistant to help building queries).

The main critiques that we can have about the aggregation framework either about the framework itself or about its accesibility in Python are the following:

* It has a steep learning curve
* It is quite verbose
* There is no Python API to use it
* It is undocumented in pymongo

`monggregate` tries to solve these issues by providing a Python API to use the aggregation framework.

The API improves the readability of the pipelines and make the queries less verbose.

It also integrates most of the official MongoDB documentation available directly in the code. Therefore, you no longer have to navigate between the documentation and your code. You no longer have to try your pipelines on Compass or Atlas to see if they work. You can do it directly in your application code. You could for example, try out your pipelines in a test suite or in a notebook.

The cherry on the cake is, your Integrated Development Environment (IDE) will help you in the process because you now have autocompletion showing you the available stages and operators, their parameters, types, descriptions and restrictions.

## **Who Should Use It ?**

The package is probably more useful for data and sofware engineers that are not familiar with the aggregation framework or that are not familiar with MongoDB in general.

However, developers that are already familiar with the aggregation framework or MongoDB may also find it useful as it can help them to build pipelines faster and with less errors.<br>
It can also improve the readability of the pipelines built.

## **How to Use It ?**

In the [following pages](../tutorial/getting-started.md), we will see how to use `monggregate` to build aggregation pipelines.
