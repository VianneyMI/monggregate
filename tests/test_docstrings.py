"""
Module to test consistency in  the documentation

The goal of those tests is to ensure that the documentation (classes docstrings) of the stages stay consistent
with the documentation of their mirrors in the Pipeline class.

"""
# Standard Library imports
#----------------------------
from copy import copy

# 3rd Party imports
# ---------------------------
import pytest
import humps

# Package imports
# ---------------------------
from monggregate import stages # pylint: disable=import-error
from monggregate import Pipeline # pylint: disable=import-error



@pytest.mark.unit
def test_dynamic_docstrings()->None:
    """
    Tests that reference docstring is included in dummy docstring.

    Prelude to ensure that the below tests will work properly.

    """

    def reference()->None:
        """Reference docstring"""

    def dummy()->None:
        """Original doctstring"""

    dummy.__doc__ += ("\n" + reference.__doc__) # type: ignore

    assert reference.__doc__ in dummy.__doc__





@pytest.mark.unit
@pytest.mark.latest
def test_sync_docstrings()->None:
    """Tests synchronization between stages classes and their mirror in the pipeline class"""

    # Exempted stages
    # --------------------------------------
    exempts = [
        "Stage", # Base class, not a real stage
        "Search", # Implementation a bit particular. Has multiple constructors
        "SearchMeta"
    ]
    # Retrieving the members of the pipeline class
    # to access them dynamically
    # --------------------------------------
    pipeline_members = Pipeline.__dict__

    # Retrieving the stages classes
    # --------------------------------------
    stages_members = stages.__dict__ # mapping between member name and members of the package
                                     # which can be functions, variables or classes


    # Filtering non-classes stages members
    stages_classes = [
        member for member in list(stages_members.keys()) 
        if member[0].isupper() and issubclass(stages_members[member], stages.Stage) and member not in exempts
        ]
    # stages_classes is a list containing the names of the class in the stages subpackage

        # FIXME: The above will break if constants are included into stages
        # we actually need something more precise to identify classes
        # to spot constants and remove them we should look for all-upper case strings

    # Iteraring over each class in stages
    for class_name in stages_classes:

        class_ = stages_members[class_name]
        assert isinstance(class_.__doc__, str) # to check is the docstring is not None
                                               # mostly to please linters

        # Keeping the actual content only
        # (i.e we allow white spaces, new lines and tabs discrepancies)
        to_check = extract_content(class_.__doc__.split("Attributes:\n    ")[-1])
        assertion = to_check in extract_content(pipeline_members[humps.decamelize(class_name)].__doc__)
        assert assertion , f"Docstring are not sync between class {class_name} and mirror pipeline method {pipeline_members[humps.decamelize(class_name)]}"

# Utility functions
# ----------------------------
def extract_content(text:str)->str:
    """Removes all white spaces, newlines and tabs from string"""

    removal_list = [' ', '\t', '\n']
    content:str = copy(text)
    for to_be_removed in removal_list:

        content = content.replace(to_be_removed, "")

    return content
