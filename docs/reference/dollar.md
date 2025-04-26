# 💲 **Dollar and DollarDollar Reference**

In MongoDB's aggregation framework, dollar signs (`$` and `$$`) have special meaning. Monggregate abstracts these with two powerful classes: `Dollar` and `DollarDollar`.

## 💲 **Dollar Class (`S`)**

The `Dollar` class is a singleton that provides an interface to MongoDB's operators and field references. It is instantiated and exported as `S`.

### 🎯 **Purpose**

1. **Operator Access**: Provides a Python interface to all MongoDB operators with proper typing and validation
2. **Field References**: Creates references to document fields using MongoDB's dollar prefix notation

### 🛠️ **Usage**

Import the `S` object:

```python
from monggregate import S
```

#### **Creating Operators**

```python
# Arithmetic operators
addition = S.add("$price", "$tax")  # Returns {"$add": ["$price", "$tax"]}
multiply = S.multiply("$quantity", "$price")  # Returns {"$multiply": ["$quantity", "$price"]}

# Comparison operators
greater_than = S.gt("$age", 18)  # Returns {"$gt": ["$age", 18]}
equals = S.eq("$status", "active")  # Returns {"$eq": ["$status", "active"]}

# Boolean operators
logic_and = S.and_([S.gt("$age", 18), S.lt("$age", 65)])

# Array operators
array_size = S.size("$tags")  # Returns {"$size": "$tags"}
```

#### **Field References**

```python
# Reference a field directly
name_field = S.name  # Returns "$name"

# Explicit field reference
price_field = S.field("price")  # Returns "$price"
```

### 🔄 **Methods vs. Attributes**

The `Dollar` class distinguishes between methods and attributes:

- **Methods** like `S.sum()`, `S.avg()`, `S.gt()` create operators
- **Attributes** like `S.name`, `S.price`, `S.customer_id` create field references

### 🗂️ **Available Operator Categories**

The `S` object provides access to these operator categories:

- **Accumulators**: `S.sum()`, `S.avg()`, `S.push()`, etc.
- **Arithmetic**: `S.add()`, `S.multiply()`, `S.divide()`, etc.
- **Array**: `S.size()`, `S.filter()`, `S.in_()`, etc.
- **Boolean**: `S.and_()`, `S.or_()`, `S.not_()`, etc.
- **Comparison**: `S.eq()`, `S.gt()`, `S.lt()`, etc.
- **Conditional**: `S.cond()`, `S.if_null()`, `S.switch()`, etc.
- **Date**: `S.millisecond()`, etc.
- **Objects**: `S.merge_objects()`, `S.object_to_array()`, etc.
- **String**: `S.concat()`, `S.date_to_string()`, etc.
- **Type**: `S.type_()`

> 📝 **Note**: Some method names differ slightly from their MongoDB counterparts to avoid Python reserved keywords. For example, `S.and_()` instead of `and` (which is a Python keyword).

## 💲💲 **DollarDollar Class (`SS`)**

The `DollarDollar` class is a singleton that provides access to MongoDB's aggregation variables (using `$$` prefix). It is instantiated and exported as `SS`.

### 🎯 **Purpose**

Provides access to:
- System aggregation variables (`$$ROOT`, `$$CURRENT`, etc.)
- User-defined variables in aggregation expressions

### 🛠️ **Usage**

Import the `SS` object:

```python
from monggregate import SS
```

#### **System Variables**

```python
# Access system variables (constants)
root = SS.ROOT       # Returns "$$ROOT"
current = SS.CURRENT # Returns "$$CURRENT"
now = SS.NOW         # Returns "$$NOW"
```

#### **User-defined Variables**

```python
# Reference user-defined variables
product = SS.product_name  # Returns "$$product_name"
customer = SS.customer_id  # Returns "$$customer_id"
```

### 🗂️ **Available System Variables**

The `SS` object provides these built-in system variables:

- `SS.CLUSTER_TIME` - Current timestamp across the deployment
- `SS.NOW` - Current datetime value
- `SS.ROOT` - The root document 
- `SS.CURRENT` - Reference to start of the field path
- `SS.REMOVE` - Conditional field exclusion
- `SS.DESCEND`, `SS.PRUNE`, `SS.KEEP` - $redact expression results

## 🌟 **Real-world Example**

This example demonstrates combining `S` and `SS` in a pipeline:

```python
from monggregate import Pipeline, S, SS

pipeline = Pipeline()

# Define the pipeline
pipeline.lookup(
    right="orders",
    left_on="_id",
    right_on="customer_id",
    name="customer_orders"
).add_fields(
    # Count total orders
    order_count=S.size("$customer_orders"),
    
    # Calculate total spent using system variables
    total_spent=S.sum(
        S.multiply(
            "$customer_orders.amount", 
            S.cond(
                S.eq("$customer_orders.status", "completed"),
                1,
                0
            )
        )
    ),
    
    # Find most expensive order
    most_expensive_order=S.max_n(
        "$customer_orders.amount", 
        1
    )
).match(
    # Filter by expression using system variable
    S.gt(S.divide("$total_spent", SS.NOW), 0.5)
)
```

## 🔄 **Comparison with Pipeline Class**

The relationship between different Monggregate abstractions:

| Class | Singleton | MongoDB Element | Purpose |
|-------|-----------|-----------------|---------|
| `Pipeline` | N/A | Aggregation Pipeline | Defines sequence of operations |
| `Stage` classes | N/A | Aggregation Stages | Individual pipeline steps |
| `Dollar` | `S` | $ Operators & References | Expressions and field references |
| `DollarDollar` | `SS` | $$ Variables | System and user variables |

> 💡 Just as `Pipeline` provides methods for all stages, the `S` object provides methods for all MongoDB operators. They serve similar roles in different contexts - `Pipeline` for constructing aggregation sequences, and `S` for building expressions with operators. 