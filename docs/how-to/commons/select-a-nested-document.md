This guide will show you how to select and return nested documents directly.

This is a common use case that one can face when working with a collection where relations are materialized by embedded documents.

We will use the `listingsAndReviews` collection from the `sample_airbnb` database.

This collection represent AirBnB listings. 
The `reviews` do not have their own collection, they are embedded in a `reviews` field in the `listingsAndReviews` collection.

## **What do we want to achieve ?**

We want to select all the reviews of a given reviewer.

## **How ?**

This can be achieved by combining three operators:

* `$unwind` to deconstruct the `reviews` array
* `$replaceRoot` to promote the `reviews` field to the root of the document
* `$match` to select the documents that match the given reviewer

Thus the following pipeline will return all the reviews of the reviewer with the `reviewer_id:2961855`:

```python

# Imports
# and boilerplate code
# to get the db object are not included

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

`documents[0]` should output:

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
## **Generalization**

This section aims at helping you adapt the above example to your own use case.

First, the `unwind` stage above is not required in case of a one-to-one embedding relation.<br> 
For example, each listing has an `address` field that contains the address of the listing. In this case, you can directly use the `address` field in the `replace_root` stage.<br>
You do not need an `unwind` stage there because the `address` field is not an array.

Second, the documents could be more deeply nested. In that case, you would need to repeat the above steps for each level of nesting. 
