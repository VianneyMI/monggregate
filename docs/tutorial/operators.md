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

## 🔮 **The `S` and `SS` Objects**

Monggregate provides two special singleton objects that abstract MongoDB's dollar sign syntax:

### 💲 **The `S` Object (Dollar)**

> 🔑 **Key Concept**: The `S` singleton directly mirrors MongoDB's `$` symbol and its dual role in the MongoDB query language.

In MongoDB, the dollar sign (`$`) has two distinct meanings:
1. As a **prefix for operators**: `{ $sum: 1 }`, `{ $gt: 10 }`
2. As a **prefix for field references**: `"$name"`, `"$address.city"`

The `S` object faithfully reproduces this dual functionality in Python:

1. **Operator Access**: Methods on `S` create MongoDB operators:
   ```python
   from monggregate import S
   
   # Create operators
   sum_op = S.sum(1)                # Becomes {"$sum": 1}
   gt_op = S.gt("$price", 100)      # Becomes {"$gt": ["$price", 100]}
   ```

2. **Field References**: Attributes of `S` create field references:
   ```python
   # These are equivalent ways to reference the "name" field
   field_ref1 = S.name       # Becomes "$name"
   field_ref2 = S.field("name")  # Also becomes "$name"
   ```

> 💡 This direct mapping to MongoDB's `$` symbol makes the transition between MongoDB query language and Monggregate's Python interface intuitive and straightforward.

#### 💪 **Why Use `S` Instead of Direct `$` Syntax?**

While you could write MongoDB queries with direct string literals containing `$` signs, using the `S` object offers significant advantages:

1. **Type Safety and Validation**:
   ```python
   # With S object - type checked, validated
   S.gt("$age", 18)
   
   # Direct syntax - no validation, easy to make typos
   {"$gt": ["$age", 18]}  # Could easily mistype as "$gte" or "$gtt"
   ```

2. **Code Completion and Documentation**:
   - IDEs can provide autocompletion for `S.sum()`, `S.gt()`, etc.
   - Documentation is accessible via docstrings and tooltips
   - No need to remember exact MongoDB syntax or consult external documentation

3. **Python-Native Interface**:
   - Use Python conventions like snake_case methods (`S.object_to_array()` vs `"$objectToArray"`)
   - Operators like `$and`, `$in` that conflict with Python keywords are available as `S.and_()`, `S.in_()`

4. **Consistent Syntax for Different Contexts**:
   - MongoDB has different syntaxes for the same operator depending on context (query vs aggregation)
   - `S` provides a unified interface regardless of where the operator is used

5. **Composability and Expressiveness**:
   ```python
   # Complex expressions are more readable with S
   S.and_([
       S.gt("$age", 18),
       S.lt("$age", 65),
       S.in_("$status", ["active", "pending"])
   ])
   
   # Versus direct syntax
   {"$and": [
       {"$gt": ["$age", 18]},
       {"$lt": ["$age", 65]},
       {"$in": ["$status", ["active", "pending"]]}
   ]}
   ```

6. **Reduced Syntax Errors**:
   - Proper nesting of operators is handled automatically
   - Correct placement of dollar signs is guaranteed
   - Parameter count and types are validated

> 🚀 The `S` object transforms MongoDB's JSON-based query language into a first-class Python experience, with all the tooling, safety, and convenience that brings.

### 💲💲 **The `SS` Object (DollarDollar)**

The `SS` object is an instance of the `DollarDollar` class that provides access to MongoDB's aggregation variables (prefixed with `$$`):

```python
from monggregate import SS

# Access system variables
root_var = SS.ROOT        # Returns "$$ROOT"
current_var = SS.CURRENT  # Returns "$$CURRENT"

# Create references to user-defined variables
product_var = SS.product_name  # Returns "$$product_name"
```

> 📘 System variables are uppercase constants on the `SS` object, while custom variables can be accessed via any attribute name.

### 🔄 **Combining `S` and `SS` in Expressions**

The real power comes when combining these objects in expressions:

```python
from monggregate import Pipeline, S, SS

pipeline = Pipeline()
pipeline.match(
    S.expr(S.eq(S.type(SS.ROOT), "array"))  # Match if the root document is an array
).project(
    items=1,
    first_item=S.arrayElemAt(SS.ROOT, 0)  # Get the first element of the root
)
```

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