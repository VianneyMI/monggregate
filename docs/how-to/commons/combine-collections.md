This guide will show you how to merge two collections.
Keep in mind that merging collections here means embedding documents from one collection into matching documents from another collection.

In the previous guide, we splitted the `listingsAndReviews` collection into two collections: `listings` and `reviews`.
We will use these two collections to show you how to merge collections.

## **What do we want to achieve ?**

We want to get a listing and its associated reviews.

## **How ?**

We will use the `$lookup` stage that was also presented in the [tutorial](../../tutorial/stages.md#usage).

```python
#/!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object
# are not included
#/!\    /!\    /!\

from monggregate import Pipeline

reviews = "reviews"

pipeline = Pipeline()
pipeline.lookup(
    right=reviews,
    left_on=reviews,
    right_on="_id",
    name=reviews
)

db["listings"].aggregate(pipeline=pipeline.export())

```

