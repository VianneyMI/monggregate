This guide will show you how to create a new collection from an existing one and to update an existing collection.

Like in the [previous how-to guide](./select-a-nested-document.md), we will use the `listingsAndReviews` collection from the `sample_airbnb` database.

## **What do we want to achieve ?**

We want to separate the reviews from the listings and to create a new collection `reviews` that will contain all the reviews while keeping the relationship between the reviews and the listings.

## **How ?**

### **Creating the new collection**

It's going to be very similar to what we have done previously.
Except that this time we will save the result of the pipeline in a new collection.

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
    reviews
    ).replace_root(
        reviews
    ).out(
        reviews
    )
# Executing the pipeline
db["listingsAndReviews"].aggregate(pipeline=pipeline.export())
# This pipeline won't output anything
```

We now have created our reviews collection. However now the reviews live in two places. The `listingsAndReviews` collection and the `reviews` collection.
In the `listingsAndReviews` collection, we want to keep only the reference to a given review in the reviews collection.

### **Updating the listingsAndReviews collection**

We want to replace the listingsAndReviews collection with a new one that will contain the reference to the reviews instead of the full review documents.

We have two options there, we can either create a new collection and drop the old one or we can update the existing collection.

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

# Showing Option 1: Creating a new collection 
# and dropping the old one
pipeline.add_fields(
    {new_field:"$reviews._id"}
    ).add_fields(
        {"reviews":f"${new_field}"}
    ).unset(
        new_field
    ).out(new_collection)

db.drop_collection(old_collection)


# Showing Option 2: Updating the existing collection

# pipeline.add_fields(
#     {new_field:"$reviews._id"}
#     ).add_fields(
#         {"reviews":f"${new_field}"}
#     ).unset(
#         new_field
#     ).out(old_collection)
# db[old_collection].rename(new_collection)
```

You should now have two distinct collections: `reviews` and `listings`.

Separating the reviews can be convenient to be able to retrieve a particular review document.
Now you can do so, by querying the `reviews` collection with MQL.
On the contrary, if you want to query a given listing with its reviews, you will have to perform a [join operation](join-operations.md) using the aggregation framework.

## **Generalization**

The `$out` stage is very useful to create new collections or update existing ones.
Alternatively, you can use the `$merge` stage to update an existing collection with more control on what happens in case of conflicts.
