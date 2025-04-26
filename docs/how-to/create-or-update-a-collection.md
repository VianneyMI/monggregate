# Creating and Updating Collections in MongoDB

This guide demonstrates how to create a new collection from an existing one and update existing collections using MongoDB's aggregation framework with monggregate.

Like in the [previous how-to guide](./select-a-nested-document.md), we will use the `listingsAndReviews` collection from the `sample_airbnb` database.

## Use Case: Normalizing Data with Collection Operations

In this example, we'll implement a common database normalization pattern: separating embedded documents into their own collection while maintaining relationships between the collections.

### Our Goal

We want to extract all reviews from the `listingsAndReviews` collection into a separate `reviews` collection while maintaining the relationship between listings and their reviews.

This separation provides several benefits:
- Improved query performance when working with review data independently
- Reduced document size in the listings collection
- Better data organization following database normalization principles

## Implementation

### Step 1: Creating the New Reviews Collection

First, we'll extract all reviews into their own collection using an aggregation pipeline:

```python
# /!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object
# are not included
# /!\    /!\    /!\
from monggregate import Pipeline

# Building the pipeline
reviews = "reviews"
pipeline = Pipeline()
pipeline.unwind(
    reviews           # Separate each review into individual documents
).replace_root(
    reviews           # Make each review the root document
).out(
    reviews           # Output to a new "reviews" collection
)
# Executing the pipeline
db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
# This pipeline won't output anything as the result is stored in the new collection
```

The pipeline above:
1. Uses `$unwind` to deconstruct the reviews array into individual documents
2. Uses `$replaceRoot` to promote each review to become the root document
3. Uses `$out` to save the results to a new "reviews" collection

After this operation, the reviews exist in both the original `listingsAndReviews` collection and our new `reviews` collection.

### Step 2: Updating the Listings Collection

Next, we'll modify the listings collection to replace full review documents with just their IDs, creating a reference-based relationship:

#### Option 1: Create a new collection and drop the old one

```python
# /!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object
# are not included
# /!\    /!\    /!\
from monggregate import Pipeline

# Useful variables
new_field = "review_ids"
new_collection = "listings"
old_collection = "listingsAndReviews"

# Building the pipeline
pipeline = Pipeline()

# Create a new collection with references instead of embedded reviews
pipeline.add_fields(
    {new_field: "$reviews._id"}    # Extract review IDs into a temporary field
).add_fields(
    {"reviews": f"${new_field}"}   # Replace reviews array with array of IDs
).unset(
    new_field                      # Remove the temporary field
).out(
    new_collection                 # Output to new "listings" collection
)

# Execute pipeline and then remove old collection
db[old_collection].aggregate(pipeline=pipeline.export())
db.drop_collection(old_collection)
```

#### Option 2: Update the existing collection in place

```python
# Option 2: Update the existing collection
pipeline = Pipeline()
pipeline.add_fields(
    {new_field: "$reviews._id"}    # Extract review IDs into a temporary field
).add_fields(
    {"reviews": f"${new_field}"}   # Replace reviews array with array of IDs  
).unset(
    new_field                      # Remove the temporary field
).out(
    old_collection                 # Overwrite the existing collection
)

# Execute pipeline and optionally rename the collection
db[old_collection].aggregate(pipeline=pipeline.export())
db[old_collection].rename(new_collection)
```

After performing either option, you'll have two properly normalized collections:
- `reviews`: Contains individual review documents with their own _id
- `listings`: Contains listings with references to reviews (just the IDs)

## Working with the New Collections

### Querying Individual Reviews

You can now easily query reviews directly without loading entire listing documents:

```python
# Find all reviews by a specific reviewer
reviewer_name = "John"
db.reviews.find({"reviewer_name": reviewer_name})
```

### Retrieving Listings with Their Reviews

To get listings with their full review data, you'll need to perform a join operation using the `$lookup` stage:

```python
from monggregate import Pipeline

pipeline = Pipeline()
pipeline.lookup(
    right="reviews",          # Target collection
    left_on="reviews",        # Field in listings containing review IDs
    right_on="_id",           # Field in reviews to match against
    name="full_reviews"       # Name for the new array of joined reviews
)

# Execute to get listings with their full reviews
db["listings"].aggregate(pipeline=pipeline.export())
```

See the [combine collections guide](combine-collections.md) for more details on joins.

## Advanced Collection Operations

### Using $out vs $merge

MongoDB provides two main stages for creating or updating collections:

- **$out**: Replaces an entire collection with the results of the pipeline. This is what we used above.
- **$merge**: Provides more granular control, allowing you to update, replace, or insert documents selectively.

For partial updates or when you need to handle document conflicts, `$merge` is generally the better choice:

```python
# Example using $merge instead of $out (pseudocode)
pipeline.merge(
    into="target_collection",     # Target collection
    on="_id",                     # Field to match documents on
    whenMatched="merge",          # How to handle matches: merge, replace, keepExisting, etc.
    whenNotMatched="insert"       # What to do with new documents
)
```

The `$merge` stage gives you fine-grained control over how documents are combined, making it ideal for incremental updates and data migrations.
