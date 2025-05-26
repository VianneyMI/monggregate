from monggregate import Pipeline

pipeline = Pipeline()
pipeline.lookup(
    right = "comments", # collection to join
    left_on = "_id",  # primary key
    right_on = "movie_id", # foreign key
    # name of the field that will contain the matching documents
    name = "related_comments" 
)

pipeline = Pipeline()
pipeline.lookup(
    right = "comments", 
    left_on = "_id", 
    right_on = "movie_id",
    name = "related_comments" 
).sort(
    by="movie_count"
).limit(
    10
)

#Le test de dit qu'il y a une erreur
#Comme quoi 'Pipeline' n'est pas défini
#Solution : importation de la fonction 'Pipeline' depuis monggregate
#Nouvelle erreur rencontrée : Pipeline.sort() takes 1 positional argument but 2 were given