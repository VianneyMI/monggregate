# Combining Collections

This guide demonstrates how to merge data from two collections using MongoDB's aggregation framework.

## Use Case

You need to combine related data from separate collections - in this case, retrieving listings along with their associated reviews.

## Prerequisites

This guide uses the collections we created in the previous guide where we split the `listingsAndReviews` collection into separate `listings` and `reviews` collections.

## Using $lookup

The `$lookup` operation performs a left outer join, allowing you to incorporate documents from one collection into matching documents from another.

```python
from monggregate import Pipeline

# Define the pipeline
pipeline = Pipeline()
pipeline.lookup(
    right="reviews",         # Target collection we're joining with
    left_on="_id",           # Field in the listings collection
    right_on="listing_id",   # Field in the reviews collection that matches
    name="reviews"           # Output field to store the joined data
)

# Execute the pipeline on the listings collection
results = db["listings"].aggregate(pipeline=pipeline.export())
```

## Result Structure

After execution, each document from the `listings` collection will contain a new `reviews` array field with all matching review documents.

## Additional Options

For more control over joined data:
- Use `pipeline.project()` after lookup to shape the output
- Add matching conditions with `let` and `pipeline` parameters
- Explore the `$unwind` stage to process array results

## Related Topics
- [Selecting Nested Documents](select-a-nested-document.md)
- [MongoDB Aggregation Framework](../../intro/mongodb-aggregation-framework.md)
