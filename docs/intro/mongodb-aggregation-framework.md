The MongoDB Aggregation Framework is an essential tool for any developer working with MongoDB. It offers advanced querying capabilities that are not available in MQL.

## **Usage**

Even if the name focuses on the aggregation part of the framework, it can actually be used for the following purposes:

1. **Data Summarization and Reporting:**

    This the actual aggregation in "aggregation framework".
    
    The aggregation framework allows you to categorize data, group documents, calculate aggregated values like totals, averages, counts, and more, with stages like `$group`, `$count`, `$bucket`, `$bucketAuto`, `$facet`, `$sortBycount`.
    
2. **Data Transformation and Enrichment:**
    
    This is one of the lesser known use cases of the framework.

    It can be used to apply complex transformations to your data, and enrich existing documents with additional information.
    The main "functions" are `$addFields`, `$densify`, `$fill`, `$replaceWith`, `$merge`, `$out`.

    You can see examples of this in [Create or update a collection](../how-to/commons/create-or-update-a-collection.md).

3. **Join-like Operations:**

    Another important feature is the ability to perform join-like operations on your data.
    
    The frameworks exposes several functions to combine data from multiple collections. You can combine collections horizontally or vertically
    respectively with the `$lookup` and `$unionWith` stages.

    See [Merge collections](../how-to/commons/combine-collections.md) for some examples.

4. **Time Series Analysis:**

    The framework also defines several operators that can be used to enhance some of the stages mentioned above.

    Among those operators, a couple of them are specifically designed to work with time series data. You can use them to group documents by time intervals, and to perform calculations on those groups.

    Such operators include `$dateAdd`, `$dateDiff`, `$millisecond`, `$toDate`, `$dateFromString`, `$dateFromParts` and much more.

    <See insert link to related How-to guides or to API Reference or to another conceptual page TODO, for an example.> 

5. **Geospatial Analysis:**

    Similarly, the framework has capabilities to perform geospatial analysis on your data. 

    In particular, you can compute distances between points, and find documents within a certain distance of a given point with the `$geoNear` stage.

6. **Textual Search and Analysis:**

    Finally, one of the most interesting features of the framework (and also one of the less expected from the name) is textual search.

    This part could be viewed as a framework on his own but, for some reason, was integrated to the aggregation framework.
    The aggregation framework leverages MongoDB Atlas full-text search capabilities. Textual search, unlike string matching, which looks for exact matches of a query term, involves finding documents that contain the query term or a related term.

    The entry points for this feature are the `$search` and `$searchMeta` stages.
    However, the reason I said this part could be viewed as a framework on his own previously is that `$search` and `$searchMeta` come with their own set operators. Such operators include `$autocomplete`, `$facet`, `$text`, `$compound` and much more.

    <See insert link to dedicated Textual Search section TODO, for more information>

## **Concepts**

The previous section makes references to several key concepts that are important to understand to use the aggregation framework.
This section will introduce those concepts and explain them in more detail.

### **Stage**

A stage is an operation on your data. It can be a querying operation, an aggregation, a transformation, a join, a textual search, a sorting operation, etc. You can view it as a function.

Stages are the building blocks of an aggregation pipeline. Each stage represents a specific data processing operation that is applied to a set of documents. These stages are arranged in a sequence to achieve the desired transformation of the data.

### **Pipeline**

A pipeline is a set of stages that are executed in sequence. The output of a stage is the input of the next stage. 
The output of the last stage is the output of the pipeline.
The input of the first stage in a pipeline is the entire set of documents of the collection targeted by the pipeline.

### **Operator**

Operators are the tools used within each stage to perform specific operations on the data. They allow for a wide range of computations, transformations, and evaluations. Examples of operators include arithmetic operators, logical operators, array operators, and more.


### **Expression**

Probably the most difficult concept to grasp is the concept of an expression. It is also the most important one.

Expressions are a bit hard to define. They are actually not even properly defined in the official MongoDB documentation.
Here how they are referred to in their documentation:

> Expressions can include field paths, literals, system variables, expression objects, and expression operators. Expressions can be nested.

The reason why it is hard to define an expression is because the concepts of expression and operator are closely related (but still distinct).

NOTE: In fact, operators produce expressions.

An expression is a more general term that refers to a combination of values, variables, and operators that, when evaluated, results in a single value or object. An expression can include one or more operators to perform computations or transformations.