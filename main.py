"""Entry point of the package"""

from pymongo import MongoClient
from app.pipeline import Pipeline
from app.stages import Match, Project


MONGODB_SERVER = "mongodb://admin:admin@localhost:27017/Kompozite?authSource=admin" # local
client = MongoClient(MONGODB_SERVER)
db = client.Kompozite


match = Match(query={"codename":"compo_51"})
projection = Project(include=set(["codename", "name", "name_fr"]), exclude=set(["_id"]))
pipeline = Pipeline(
    db = db,
    collection = "components",
    stages = [match, projection]
)

if __name__ == "__main__":
    print("It's Ok !")
    print(pipeline())
