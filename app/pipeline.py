"""Pipeline Module"""

from typing import Any
from pymongo.database import Database
from pydantic import BaseModel, BaseConfig
from app.stages import (
    Stage,
    Bucket, BucketAuto,
    Count, Group, Limit,
    Match, Project,
    ReplaceRoot,
    Sample,
    Set, Skip,
    Sort, SortByCount,
    Unwind
)


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
            print(stage())
            stages.append(stage())


        array = list(self.db[self.collection].aggregate(pipeline=stages))
        return array

    def bucket(self, **kwargs:Any)->"Pipeline":
        """Adds a bucket stage to the current pipeline"""

        self.stages.append(
            Bucket(**kwargs)
        )
        return self

    def bucket_auto(self, **kwargs:Any)->"Pipeline":
        """Adds a bucket_auto stage to the current pipeline"""

        self.stages.append(
            BucketAuto(**kwargs)
        )
        return self


    def count(self, **kwargs:Any)->"Pipeline":
        """Adds a count stage to the current pipeline"""

        self.stages.append(
                Count(**kwargs)
            )
        return self

    def group(self, **kwargs:Any)->"Pipeline":
        """Adds a group stage to the current pipeline"""

        self.stages.append(
                Group(**kwargs)
            )
        return self

    def limit(self, **kwargs:Any)->"Pipeline":
        """Adds a limit stage to the current pipeline"""

        self.stages.append(
                Limit(**kwargs)
            )
        return self

    def match(self, **kwargs:Any)->"Pipeline":
        """Adds a match stage to the current pipeline"""

        self.stages.append(
                Match(**kwargs)
            )
        return self

    def project(self, **kwargs:Any)->"Pipeline":
        """Adds a project stage to the current pipeline"""

        self.stages.append(
                Project(**kwargs)
            )
        return self

    def replace_root(self, **kwargs:Any)->"Pipeline":
        """Adds a replace_root stage to the current pipeline"""

        self.stages.append(
                ReplaceRoot(**kwargs)
            )
        return self

    def sample(self, **kwargs:Any)->"Pipeline":
        """Adds a sample stage to the current pipeline"""

        self.stages.append(
                Sample(**kwargs)
            )
        return self

    def set(self, **kwargs:Any)->"Pipeline":
        """Adds a set stage to the current pipeline"""

        self.stages.append(
                Set(**kwargs)
            )
        return self

    def skip(self, **kwargs:Any)->"Pipeline":
        """Adds a skip stage to the current pipeline"""

        self.stages.append(
                Skip(**kwargs)
            )
        return self

    def sort(self, **kwargs:Any)->"Pipeline":
        """Adds a sort stage to the current pipeline"""

        self.stages.append(
                Sort(**kwargs)
            )
        return self

    def sort_by_count(self, **kwargs:Any)->"Pipeline":
        """Adds a sort_by_count stage to the current pipeline"""

        self.stages.append(
                SortByCount(**kwargs)
            )
        return self

    def unwind(self, **kwargs:Any)->"Pipeline":
        """Adds a unwind stage to the current pipeline"""

        self.stages.append(
                Unwind(**kwargs)
            )
        return self


    class Config(BaseConfig):
        """Configuration Class for Pipeline"""
        arbitrary_types_allowed = True



if __name__ == "__main__":
    pipeline = Pipeline(stages=[])
    pipeline()
