"""Pipeline Module"""

from typing import Any
from pymongo.database import Database
from pydantic import BaseModel, BaseConfig
from app.stages.stage import Stage



class Pipeline(BaseModel):
    """MongoDB aggregation pipeline abstraction"""

    db : Database # TODO : Make private
    collection : str
    stages : list[Stage] = []

    def __call__(self)->list[dict]:
        """Makes a pipeline instance callable and executes the entire pipeline when called"""

        return self.run()


    def run(self)->list[dict]:
        """Executes the entire pipeline"""

        stages = []
        for stage in self.stages:
            print(stage.statement)
            stages.append(stage.statement)


        array = list(self.db[self.collection].aggregate(pipeline=stages))
        return array


    class Config(BaseConfig):
        """Configuration Class for Pipeline"""
        arbitrary_types_allowed = True



if __name__ == "__main__":
    pipeline = Pipeline(stages=[])
    pipeline()
