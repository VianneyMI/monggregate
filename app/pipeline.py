"""Pipeline Module"""

from typing import Any
from pymongo.database import Database
from pydantic import BaseModel, BaseConfig
from app.stages import (
    Stage,
    Bucket, BucketAuto,
    Count, Group, Limit,Lookup,
    Match, Project,
    ReplaceRoot,
    Sample,
    Set, Skip,
    Sort, SortByCount,
    Unwind
)
from app.utils import StrEnum


class OnCallEnum(StrEnum):
    """Possible behaviors on pipeline call"""

    RUN = "run"
    EXPORT = "export"


class Pipeline(BaseModel):
    """MongoDB aggregation pipeline abstraction"""

    db : Database # TODO : Make private
    on_call : OnCallEnum = OnCallEnum.EXPORT
    collection : str
    stages : list[Stage] = []

    class Config(BaseConfig):
        """Configuration Class for Pipeline"""
        arbitrary_types_allowed = True

    # ------------------------------------------------
    # Pipeline Internal Methods
    #-------------------------------------------------

    def __call__(self)->list[dict]:
        """Makes a pipeline instance callable and executes the entire pipeline when called"""

        _on_call_map = {
            OnCallEnum.EXPORT:self.export,
            OnCallEnum.RUN:self.run
        }

        return _on_call_map[self.on_call]()


    def run(self)->list[dict]:
        """Executes the entire pipeline"""

        stages = self.export()
        array = list(self.db[self.collection].aggregate(pipeline=stages))

        return array


    def export(self)->list[dict]:
        """
        Exports current pipeline to pymongo format.

            >>> pipeline = Pipeline().match(...).project(...).limit(...).export()
            >>> db.examples.aggregate(pipeline=pipeline)

        """

        stages = []
        for stage in self.stages:
            stages.append(stage())

        return stages


    def to_statements(self)->list[dict]:
        """Alias for export method"""

        return self.export()


    #-----------------------------------------------------------
    # Stages
    #-----------------------------------------------------------
    def add_fields(self, **kwargs:Any)->"Pipeline":
        """Adds an add_fields stage to the current pipeline"""

        self.stages.append(
            Set(**kwargs)
        )
        return self

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

    def explode(self, **kwargs:Any)->"Pipeline":
        """Adds a unwind stage to the current pipeline"""

        self.stages.append(
                Unwind(**kwargs)
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

    def lookup(self, **kwargs:Any)->"Pipeline":
        """Adds a lookup stage to the current pipeline"""

        self.stages.append(
            Lookup(**kwargs)
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

    def replace_with(self, **kwargs:Any)->"Pipeline":
        """Adds a replace_with stage to the current pipeline"""

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


if __name__ == "__main__":
    pipeline = Pipeline(stages=[])
    pipeline()
