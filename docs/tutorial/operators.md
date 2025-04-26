# 🛠️ **MongoDB Operators in Monggregate**

MongoDB operators are the building blocks of aggregation stages, providing powerful data transformation capabilities. Monggregate makes these operators accessible through an intuitive Python interface.

## 🧠 **Understanding Operators**

### 🔄 **Relationship with Stages**

> 💡 Operators and stages work together in a MongoDB aggregation pipeline.

- **Optional but powerful**: Some stages (like `Match`) can function without operators, while others (like `Group`) require operators to be useful
- **Parallel usage**: Unlike stages which are executed sequentially, multiple operators can be used simultaneously within a single stage
- **Different syntax**: Operators in aggregation pipelines often have different syntax than their MongoDB Query Language (MQL) counterparts

### 📊 **Example: Operators in Action**

Consider this simple example that counts and collects movie titles by year:

```python
from monggregate import Pipeline, S

pipeline = Pipeline()
pipeline.group(
    by="year",
    query={
        "movie_count": S.sum(1),        # Count movies per year
        "movie_titles": S.push("$title") # Collect all titles for each year
    }
)
```

## 🚀 **Using Operators in Monggregate**

Monggregate provides two ways to access operators:

1. **Direct import**:
   ```python
   from monggregate.operators import Sum, Push
   
   sum_operator = Sum(1)
   push_operator = Push("$title")
   ```

2. **Using the `S` shortcut** (recommended):
   ```python
   from monggregate import S
   
   sum_operator = S.sum(1)
   push_operator = S.push("$title")
   ```

> 🔍 The `S` shortcut is particularly convenient as it provides access to all operators through a single import.

## 🔗 **Operator Compatibility**

Each operator is designed to work with specific stages. Monggregate's documentation includes compatibility information for each operator.

For example, the `$mergeObjects` operator can only be used in these stages:
- `$bucket`
- `$bucketAuto`
- `$group`
- `$replaceRoot`

## 🌟 **Advanced Example: Multiple Operators**

This example demonstrates using multiple operators together to analyze movie data:

```python
from monggregate import Pipeline, S

# Creating the pipeline
pipeline = Pipeline()

# Using multiple operators together
pipeline.match(
    year=S.type_("number")  # Filter for documents where year is a number
).group(
    by="year",
    query={
        "movie_count": S.sum(1),                # Count movies per year
        "avg_runtime": S.avg("$runtime"),       # Calculate average runtime
        "movie_titles": S.push("$title"),       # Collect all titles
        "genres": S.addToSet("$genres")         # Collect unique genres
    }
).match(
    movie_count=S.gt(10)                        # Filter for years with >10 movies
).sort(
    by="movie_count", 
    descending=True
)
```

## 🧩 **Complex Example: Using Expressions**

> 📘 Operators can be combined to create complex expressions.

```python
from monggregate import Pipeline, S

# Define a complex expression
comments_count = S.size("$comments")
has_many_comments = S.gt(comments_count, 5)
is_recent = S.gt("$year", 2000)

# Create pipeline using the expression
pipeline = Pipeline()
pipeline.lookup(
    right="comments",
    right_on="movie_id",
    left_on="_id",
    name="comments"
).add_fields(
    comments_count=comments_count,
    is_popular=S.and_([has_many_comments, is_recent])
).match(
    is_popular=True
)
```

## 📋 **Available Operators**

Monggregate supports all major MongoDB operators, organized by category:

### 📊 **Accumulators**
- `$avg` - Calculate average value
- `$count` - Count documents
- `$first` - Return first value in a group
- `$last` - Return last value in a group
- `$max` - Return maximum value
- `$min` - Return minimum value
- `$push` - Append values to an array
- `$sum` - Calculate sum

### 🧮 **Arithmetic**
- `$add` - Addition
- `$divide` - Division
- `$multiply` - Multiplication
- `$pow` - Exponentiation
- `$subtract` - Subtraction

### 📝 **Array**
- `$arrayToObject` - Convert array to object
- `$filter` - Filter array elements
- `$first` - Return first array element
- `$in` - Check if value exists in array
- `$isArray` - Check if value is an array
- `$last` - Return last array element
- `$max_n` - Return n maximum values
- `$min_n` - Return n minimum values
- `$size` - Get array length
- `$sortArray` - Sort array elements

### ⚖️ **Boolean**
- `$and` - Logical AND
- `$not` - Logical NOT
- `$or` - Logical OR

### 🔍 **Comparison**
- `$cmp` - Compare values
- `$eq` - Equal to
- `$gt` - Greater than
- `$gte` - Greater than or equal to
- `$lt` - Less than
- `$lte` - Less than or equal to
- `$ne` - Not equal to

### 🔀 **Conditional**
- `$cond` - Conditional expression
- `$ifNull` - Replace null values
- `$switch` - Switch statement

### 📅 **Date**
- `$millisecond` - Extract milliseconds
- `$dateFromString` - Convert string to date
- `$dateToString` - Convert date to string

### 🧱 **Object**
- `$mergeObjects` - Combine multiple documents
- `$objectToArray` - Convert object to array

### 📝 **String**
- `$concat` - Concatenate strings
- `$dateFromString` - Parse date from string
- `$dateToString` - Format date as string

### 🔍 **Search**
> 📚 For search-specific operators, see the [Search documentation](search.md).

## 🔄 **MQL vs. Aggregation Pipeline Syntax**

> ℹ️ Some operators have different syntax in MQL queries versus aggregation pipelines.

### **Example: Greater Than or Equal (`$gte`)**

In an MQL query:
```python
{
    "year": {"$gte": 2010}  # Find documents where year >= 2010
}
```

In an aggregation pipeline:
```python
{
    "$gte": ["$year", 2010]  # Compare if year field value >= 2010
}
```

With Monggregate, the syntax is unified and simplified:
```python
from monggregate import S

# In a match stage
pipeline.match(year=S.gte(2010))

# In an expression
is_recent = S.gte("$year", 2010)
```

This consistent interface helps developers avoid the complexity of different syntaxes for the same logical operations.