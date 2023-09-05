"""Module to tests the code snippet in the readme file."""

def test_basic_pipeline_usage():
    """Tests basic pipeline usage example.
    
    (First code snippet)
    """

    import os

    from dotenv import load_dotenv 
    import pymongo
    from monggregate import Pipeline, S

    # Creating connexion string securely
    load_dotenv(verbose=True)
    PWD = os.environ["MONGODB_PASSWORD"]
    MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"

    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)

    # Get a reference to the "sample_mflix" database:
    db = client["sample_mflix"]

    # Creating the pipeline
    pipeline = Pipeline()

    # The below pipeline will return the most recent movie with the title "A Star is Born"
    pipeline.match(
        title="A Star Is Born"
    ).sort(
        by="year"
    ).limit(
        value=1
    )

    # Executing the pipeline
    curosr = db["movies"].aggregate(pipeline.export())

    results = list(curosr)
    assert results

def test_advanced_usage():
    """Tests more advanced pipeline usage example.
    
    (Second code snippet)
    """

    import os

    from dotenv import load_dotenv 
    import pymongo
    from monggregate import Pipeline, S

    # Creating connexion string securely
    load_dotenv(verbose=True)
    PWD = os.environ["MONGODB_PASSWORD"]
    MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"


    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)

    # Get a reference to the "sample_mflix" database:
    db = client["sample_mflix"]


    # Creating the pipeline
    pipeline = Pipeline()
    pipeline.match(
        year=S.type_("number") # Filtering out documents where the year field is not a number
    ).group(
        by="year",
        query = {
            "movie_count":S.sum(1), # Aggregating the movies per year
            "movie_titles":S.push("$title")
        }
    ).sort(
        by="_id",
        descending=True
    ).limit(10)

    # Executing the pipeline
    cursor = db["movies"].aggregate(pipeline.export())
    
    # Printing the results
    results = list(cursor)
    #print(results)
    assert results

def test_even_more_advanced_usage():
    """Tests even more advanced pipeline usage example.
    
    (Third code snippet)

    """

    import os

    from dotenv import load_dotenv 
    import pymongo
    from monggregate import Pipeline, S, Expression

    # Creating connexion string securely
    load_dotenv(verbose=True)
    PWD = os.environ["MONGODB_PASSWORD"]
    MONGODB_URI = f"mongodb+srv://dev:{PWD}@myserver.xciie.mongodb.net/?retryWrites=true&w=majority"


    # Connect to your MongoDB cluster:
    client = pymongo.MongoClient(MONGODB_URI)

    # Get a reference to the "sample_mflix" database:
    db = client["sample_mflix"]

    # Using expressions
    comments_count = Expression.field("comments").size()


    # Creating the pipeline
    pipeline = Pipeline()
    pipeline.lookup(
        right="comments",
        right_on="movie_id",
        left_on="_id",
        name="comments"
    ).add_fields(
        comments_count=comments_count
    ).match(
        query={"$expr":comments_count>2}
    ).limit(1)

    # Executing the pipeline
    cursor = db["movies"].aggregate(pipeline.export())

    # Printing the results
    results = list(cursor)
    #print(results)
    assert results, results

if __name__ == "__main__":
    test_basic_pipeline_usage()
    test_advanced_usage()
    test_even_more_advanced_usage()
    print("Everything passed")