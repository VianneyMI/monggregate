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

pipeline.add_fields(
    {new_field:"$reviews._id"}
    ).add_fields(
        {"reviews":f"${new_field}"}
    ).unset(
        new_field
    ).out(old_collection)
db[old_collection].rename(new_collection)