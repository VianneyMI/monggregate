"""Pipeline Module"""

from typing import Any
from pymongo.database import Database
from pydantic import BaseModel, BaseConfig
from app.stage import Stage


class Pipeline(BaseModel):
    """MongoDB aggregation pipeline abstraction"""

    __db__ : Database
    collection : str
    stages : list[Stage] = []

    def __call__(self)->None:
        """Makes a pipeline instance callable and executes the entire pipeline when called"""

        self.run()

    def run(self)->Any:
        """Executes the entire pipeline"""

        for stage in self.stages:
            stage() # FIXME : stages is now a list of instances of stages

    class Config(BaseConfig):
        """Configuration Class for Pipeline"""
        arbitrary_types_allowed = True



if __name__ == "__main__":
    pipeline = Pipeline(stages=[])
    pipeline()
