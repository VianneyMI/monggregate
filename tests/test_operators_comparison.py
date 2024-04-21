"""Module gathering the tests of the comparison operators"""

# pylint: disable=import-error
import pytest
from monggregate.operators.comparison import(
   Cmp, cmp,
   Eq, eq,
   Gt, gt,
   Gte, gte,
   Lt, lt,
   Lte, lte,
   Ne, ne
)

@pytest.mark.operators
@pytest.mark.unit
@pytest.mark.functional
class TestBooleanOperators:
    """This class only aims at reusing the markers"""

    def test_cmp(self)->None:
        """Tests the $cmp operator class and mirror function"""

        cmp_op = Cmp(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert cmp_op

        # Functional test
        # -------------------
        assert cmp_op.operand == cmp("$qty", 250).operand == {
            "$cmp" : ["$qty", 250]
        }

    def test_eq(self)->None:
        """Tests the $eq operator class and mirror function"""

        eq_op = Eq(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert eq_op

        # Functional test
        # -------------------
        assert eq_op.operand == eq("$qty", 250).operand == {
            "$eq" : ["$qty", 250]
        }

    def test_gt(self)->None:
        """Tests the $gt operator class and mirror function"""

        gt_op = Gt(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert gt_op

        # Functional test
        # -------------------
        assert gt_op.operand == gt("$qty", 250).operand == {
            "$gt" : ["$qty", 250]
        }

    def test_gte(self)->None:
        """Tests the $gte operator class and mirror function"""

        gte_op = Gte(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert gte_op

        # Functional test
        # -------------------
        assert gte_op.operand == gte("$qty", 250).operand == {
            "$gte" : ["$qty", 250]
        }

    def test_lt(self)->None:
        """Tests the $lt operator class and mirror function"""

        lt_op = Lt(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert lt_op

        # Functional test
        # -------------------
        assert lt_op.operand == lt("$qty", 250).operand == {
            "$lt" : ["$qty", 250]
        }

    def test_lte(self)->None:
        """Tests the $lte operator class and mirror function"""

        lte_op = Lte(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert lte_op

        # Functional test
        # -------------------
        assert lte_op.operand == lte("$qty", 250).operand == {
            "$lte" : ["$qty", 250]
        }

    def test_ne(self)->None:
        """Tests the $ne operator class and mirror function"""

        ne_op = Ne(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert ne_op

        # Functional test
        # -------------------
        assert ne_op.operand == ne("$qty", 250).operand == {
            "$ne" : ["$qty", 250]
        }
