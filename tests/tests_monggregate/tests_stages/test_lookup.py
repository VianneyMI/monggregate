"""Tests for the Lookup stage."""

import pytest
from monggregate.stages import Lookup


class TestLookup:
    """Tests for the Lookup stage."""

    def test_instantiation(self) -> None:
        """Test that the Lookup stage can be instantiated."""
        lookup = Lookup(
            right="right_collection",
            left_on="foreign_field_id",
            right_on="_id",
            name="foreign_documents",
        )
        assert isinstance(lookup, Lookup)

    def test_expression(self) -> None:
        """Test that the expression method returns the correct expression."""

        lookup = Lookup(
            right="right_collection",
            left_on="foreign_field_id",
            right_on="_id",
            name="foreign_documents",
        )
        # fmt: off
        assert lookup.expression == {
            "$lookup": {
                "from": "right_collection",
                "localField": "foreign_field_id",
                "foreignField": "_id",
                "as": "foreign_documents",
            }
        }
        # fmt: on

    pytest.mark.xfail(reason="This should be valid. Bug in the code.")

    # NOTE: The bug is that left_on and right_on are required in the code while they should
    # be optional in that case.
    def test_expression_with_correlated_subquery(self) -> None:
        """Test that the expression method returns the correct expression."""

        lookup = Lookup(
            right="right_collection",
            let={"variable": "$local_variable"},
            pipeline=[
                {
                    "$match": {
                        "$expr": {"$gte": ["$$variable", "$foreign_field_quantity"]}
                    }
                }
            ],
            name="foreign_documents",
        )
        # fmt: off
        assert lookup.expression == {
            "$lookup": {
                "from": "right_collection",
                "let": {"variable": "$local_variable"},
                "pipeline": [{"$match": {"$expr": {"$gte": ["$$variable", "$foreign_field_quantity"]}}}],
                "as": "foreign_documents",
            }
        }
        # fmt: on

    pytest.mark.xfail(reason="This should be valid. Bug in the code.")

    # NOTE: The bug is that left_on and right_on are required in the code while they should
    # be optional in that case.
    def test_expression_with_uncorrelated_subquery(self) -> None:
        """Test that the expression method returns the correct expression."""

        lookup = Lookup(
            right="holidays",
            pipeline=[
                {"$match": {"year": 2018}},
                {"$project": {"name": 1, "date": 1, "_id": 0}},
            ],
            name="holidaysIn2018",
        )

        # fmt: off
        assert lookup.expression == {
            "$lookup": {
                "from": "holidays",
                "pipeline": [{"$match": {"year": 2018}}, {"$project": {"name": 1, "date": 1, "_id": 0}}],
                "as": "holidaysIn2018",
            }
        }
        # fmt: on


#         db.absences.aggregate([
#    {
#       $lookup: {
#          from: "holidays",
#          pipeline: [
#             { $match: { year: 2018 } },
#             { $project: { name: 1, date: 1, _id: 0 } }
#          ],
#          as: "holidaysIn2018"
#       }
#    }
# ])
