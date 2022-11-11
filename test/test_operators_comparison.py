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
        """Testes the $cmp operator class and mirror function"""

        cmp_op = Cmp(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert cmp_op

        # Functional test
        # -------------------
        assert cmp_op.statement == cmp("$qty", 250) == {
            "$cmp" : ["$qty", 250]
        }

    def test_eq(self)->None:
        """Testes the $eq operator class and mirror function"""

        eq_op = Eq(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert eq_op

        # Functional test
        # -------------------
        assert eq_op.statement == eq("$qty", 250) == {
            "$eq" : ["$qty", 250]
        }

    def test_gt(self)->None:
        """Testes the $gt operator class and mirror function"""

        gt_op = Gt(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert gt_op

        # Functional test
        # -------------------
        assert gt_op.statement == gt("$qty", 250) == {
            "$gt" : ["$qty", 250]
        }

    def test_gte(self)->None:
        """Testes the $gte operator class and mirror function"""

        gte_op = Gte(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert gte_op

        # Functional test
        # -------------------
        assert gte_op.statement == gte("$qty", 250) == {
            "$gte" : ["$qty", 250]
        }

    def test_lt(self)->None:
        """Testes the $lt operator class and mirror function"""

        lt_op = Lt(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert lt_op

        # Functional test
        # -------------------
        assert lt_op.statement == lt("$qty", 250) == {
            "$lt" : ["$qty", 250]
        }

    def test_lte(self)->None:
        """Testes the $lte operator class and mirror function"""

        lte_op = Lte(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert lte_op

        # Functional test
        # -------------------
        assert lte_op.statement == lte("$qty", 250) == {
            "$lte" : ["$qty", 250]
        }

    def test_ne(self)->None:
        """Testes the $ne operator class and mirror function"""

        ne_op = Ne(
            left = "$qty",
            right = 250
        )

        # Unit test
        # -------------------
        assert ne_op

        # Functional test
        # -------------------
        assert ne_op.statement == ne("$qty", 250) == {
            "$ne" : ["$qty", 250]
        }
