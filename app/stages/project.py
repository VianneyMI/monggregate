"""
Module defining an interface to MongoDB $project stage operation in aggregation pipeline

Online MongoDB documentation:
---------------------------------------------------------------------------------------
Last Updated :
Source : https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project


"""

# NOTE : This is a first prototype, there are so much that can be done by $project that this will be completed
# after further reading the doc and copying here and
# after having prototype more stages

# NOTE : Would be nice and useful to have something keywords arguments based to generate the projection <VM, 16/09/2022>
# (on top[on the side] of the below)

from app.stages.stage import Stage

class Project(Stage):
    """"

    """

    statement : dict
    include : set[str] # | dict for nested documents
    exclude : set[str] # | dict
