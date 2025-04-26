This guide shows how to extract and work with nested documents in MongoDB.

## When to Use This

This approach is useful when working with collections that embed related documents instead of using separate collections. Common examples include:

- Comments embedded in blog posts
- Reviews embedded in product listings
- Address details embedded in user profiles

## Example: Finding Reviews by a Specific Reviewer

We'll use the `listingsAndReviews` collection from the `sample_airbnb` database, where reviews are embedded within listing documents.

### The Pipeline Approach

To extract all reviews by a specific reviewer, we'll use three stages:

1. `$unwind`: Deconstruct the `reviews` array into individual documents
2. `$replaceRoot`: Promote each review to become the root document
3. `$match`: Filter for the specific reviewer

```python
# /!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object 
# are not included
# /!\    /!\    /!\

# The reviewer_id whose reviews we want to retrieve
reviewer_id = "2961855"

# Building the pipeline
pipeline = Pipeline()
pipeline.unwind(
    "reviews"
    ).replace_root(
        "reviews"
    ).match(
        reviewer_id=reviewer_id
    )

# Executing the pipeline
cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
documents = list(cursor)
```

### Sample Result

The first document in our results:

```python
{
    '_id': '197072826',
    'date': datetime.datetime(2017, 9, 24, 4, 0),
    'listing_id': '18776184',
    'reviewer_id': '2961855',
    'reviewer_name': 'Uge',
    'comments': 'Our stay at Alfredo’s place was amazing. \n\nThe place is spacious, very clean, comfortable, decorated with good taste, and has everything one may need. I really liked his apartment. \n\nIt is very well located, the restaurants and bars around are great and in an easy 30 minute walk you are downtown or in old Montreal. Very pleasant area to be outside and felt very safe. \n\nAlfredo always answered my messages within 5 minutes and was incredibly helpful and generous. \n\nI highly recommend this place. Thank you Alfredo!'
}
```

## Adapting to Other Scenarios

### One-to-One Relationships

For non-array nested fields like `address`, skip the `unwind` stage:

```python
# Extract address documents from listings
pipeline = Pipeline()
pipeline.replace_root(
    "address"
).match(
    country="United States"
)

cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
addresses = list(cursor)
```

### Deep Nesting

For deeply nested structures, chain multiple operations:

```python
# Access amenities.details.highlights (hypothetical nested structure)
pipeline = Pipeline()
pipeline.unwind(
    "amenities"
).replace_root(
    "amenities.details"
).unwind(
    "highlights"
).replace_root(
    "highlights"
).match(
    featured=True
)

cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
```

### Preserving Context

To keep information from the parent document:

```python
# Keep listing name while working with reviews
pipeline = Pipeline()
pipeline.project({
    "listing_name": 1, 
    "review": "$reviews"
}).unwind(
    "review"
).match(
    "review.reviewer_id": "2961855"
)

# Result includes both the review and the listing name
cursor = db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
```
