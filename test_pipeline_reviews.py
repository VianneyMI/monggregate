#/!\    /!\    /!\
# Imports
# and boilerplate code
# to get the db object
# are not included
#/!\    /!\    /!\

from monggregate import Pipeline
from pymongo import MongoClient

client = pymongo.MongoClient(MONGODB_URI)
db = client["sample_mflix"] 

reviews = "reviews"

pipeline = Pipeline()
pipeline.lookup(
    right=reviews,
    left_on=reviews,
    right_on="_id",
    name=reviews
)

db["listings"].aggregate(pipeline=pipeline.export())
db.drop_collection()
