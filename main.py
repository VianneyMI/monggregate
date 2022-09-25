"""Entry point of the package"""

from pymongo import MongoClient
from app.pipeline import Pipeline
from app.stages import Match, Project, Group, Count, Sort


MONGODB_SERVER = "mongodb://admin:admin@localhost:27017/Kompozite?authSource=admin" # local
client = MongoClient(MONGODB_SERVER)
db = client.Kompozite


#match = Match(query={"codename":"compo_51"})
#projection = Project(include=set(["codename", "name", "name_fr"]), exclude=set(["_id"]))

# group = Group(by="$category", query={"total":{"$count":{}}})
# sort = Sort(ascending=set(["_id"]))

# pipeline = Pipeline(
#     db = db,
#     collection = "PU05",
#     stages = [group, sort]
# )

if __name__ == "__main__":
    pipeline = Pipeline(
        _db=db,
        collection="PU02"
        ).match(
            query={"category":"PU02C01"}
        ).limit(
            value=3
        )()

    print("It's Ok !")
