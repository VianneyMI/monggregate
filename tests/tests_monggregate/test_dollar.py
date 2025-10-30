import pytest
from monggregate.dollar import (
    AggregationVariableEnum,
    Dollar,
    DollarDollar,
    CLUSTER_TIME,
    NOW,
    ROOT,
    CURRENT,
    REMOVE,
    DESCEND,
    PRUNE,
    KEEP,
    CONSTANTS,
    S,
    SS,
)


class TestAggregationVariableEnum:
    """Tests consistency of the `AggregationVariableEnum` class."""

    def test_members_consistency(self):
        """Tests consistency betweew the keys and the values of the enum."""

    # Iterate over the members of the enum
    checks = []
    wrong_members = []

    for key, value in AggregationVariableEnum.__members__.items():
        if key == value.value.replace("$$", ""):
            checks.append(True)
        else:
            checks.append(False)
            wrong_members.append((key, value.value))

    assert all(checks), f"The following members are not consistent: {wrong_members}"

    def test_constants_consistency(self):
        """Tests consistency of the constants in the `dollar` module."""

        # assert len(CONSTANTS) == len(AggregationVariableEnum.__members__)

        checks_constants_in_enum = []
        checks_enum_in_constants = []
        missing_constants_in_enum = []
        missing_enum_in_constants = []

        for constant in CONSTANTS:
            if constant in AggregationVariableEnum.__members__.values():
                checks_constants_in_enum.append(True)
            else:
                checks_constants_in_enum.append(False)
                missing_constants_in_enum.append(constant)

        for enum in AggregationVariableEnum.__members__.values():
            if enum.value in CONSTANTS:
                checks_enum_in_constants.append(True)
            else:
                checks_enum_in_constants.append(False)
                missing_enum_in_constants.append(enum.value)

        error_message = "Inconsistency between the constants and the enum: \n"
        if missing_constants_in_enum:
            error_message += f"  * The following constants are not in the enum: {missing_constants_in_enum}\n"
        if missing_enum_in_constants:
            error_message += f"  * The following enum values are not in the constants: {missing_enum_in_constants}\n"

        assert all(checks_constants_in_enum) and all(checks_enum_in_constants), (
            error_message
        )


class TestDollar:
    """Test the Dollar class."""

    def test_instantiation(self):
        """Test that Dollar class can be accessed correctly and returns dollar-prefixed fields."""

        dollar = Dollar()
        assert isinstance(dollar, Dollar)

    def test_singleton(self):
        """Test that Dollar class is a singleton."""

        assert Dollar() is Dollar()
        assert Dollar() is S

    def test____getattr__(self):
        """Test the __getattr__ method of the Dollar class."""

        # Test field reference
        assert Dollar().name == "$name"

    def test_field(self):
        """Test the field() method of the Dollar class."""

        # Test field() method
        assert Dollar().field("price") == "$price"

    # -----------------------------------
    # Test accumulator methods
    # -----------------------------------
    
    def test_avg(self):
        """Test the avg() method of the Dollar class."""
        from monggregate.operators.accumulators import Avg
        
        result = Dollar.avg("$price")
        assert isinstance(result, Avg)
        
    def test_count(self):
        """Test the count() method of the Dollar class."""
        from monggregate.operators.accumulators import Count
        
        result = Dollar.count()
        assert isinstance(result, Count)
        
    def test_first(self):
        """Test the first() method of the Dollar class."""
        from monggregate.operators.accumulators import First
        
        result = Dollar.first("$name")
        assert isinstance(result, First)
        
    def test_last(self):
        """Test the last() method of the Dollar class."""
        from monggregate.operators.accumulators import Last
        
        result = Dollar.last("$name")
        assert isinstance(result, Last)
        
    def test_max(self):
        """Test the max() method of the Dollar class."""
        from monggregate.operators.accumulators import Max
        
        result = Dollar.max("$price")
        assert isinstance(result, Max)
        
    def test_min(self):
        """Test the min() method of the Dollar class."""
        from monggregate.operators.accumulators import Min
        
        result = Dollar.min("$price")
        assert isinstance(result, Min)
        
    def test_push(self):
        """Test the push() method of the Dollar class."""
        from monggregate.operators.accumulators import Push
        
        result = Dollar.push("$item")
        assert isinstance(result, Push)
        
    def test_sum(self):
        """Test the sum() method of the Dollar class."""
        from monggregate.operators.accumulators import Sum
        
        result = Dollar.sum("$amount")
        assert isinstance(result, Sum)
        
    # -----------------------------------
    # Test arithmetic methods
    # -----------------------------------
    
    def test_add(self):
        """Test the add() method of the Dollar class."""
        from monggregate.operators.arithmetic import Add
        
        result = Dollar.add("$a", "$b")
        assert isinstance(result, Add)
        
    def test_divide(self):
        """Test the divide() method of the Dollar class."""
        from monggregate.operators.arithmetic import Divide
        
        result = Dollar.divide("$a", "$b")
        assert isinstance(result, Divide)
        
    def test_multiply(self):
        """Test the multiply() method of the Dollar class."""
        from monggregate.operators.arithmetic import Multiply
        
        result = Dollar.multiply("$a", "$b")
        assert isinstance(result, Multiply)
        
    def test_pow(self):
        """Test the pow() method of the Dollar class."""
        from monggregate.operators.arithmetic import Pow
        
        result = Dollar.pow("$base", "$exponent")
        assert isinstance(result, Pow)
        
    # Note: subtract method doesn't exist in Dollar class, skipping this test
        
    # -----------------------------------
    # Test array methods
    # -----------------------------------
    
    def test_array_to_object(self):
        """Test the array_to_object() method of the Dollar class."""
        from monggregate.operators.array import ArrayToObject
        
        result = Dollar.array_to_object("$array")
        assert isinstance(result, ArrayToObject)
        
    def test_filter(self):
        """Test the filter() method of the Dollar class."""
        from monggregate.operators.array import Filter
        
        # The filter method has different signature: filter(operand, let, query, limit=None)
        result = Dollar.filter("$array", let="item", query={"$gt": ["$$item", 5]})
        assert isinstance(result, Filter)
        
    def test_in_(self):
        """Test the in_() method of the Dollar class."""
        from monggregate.operators.array import In
        
        result = Dollar.in_("$item", "$array")
        assert isinstance(result, In)
        
    def test_is_array(self):
        """Test the is_array() method of the Dollar class."""
        from monggregate.operators.array import IsArray
        
        result = Dollar.is_array("$field")
        assert isinstance(result, IsArray)
        
    def test_size(self):
        """Test the size() method of the Dollar class."""
        from monggregate.operators.array import Size
        
        result = Dollar.size("$array")
        assert isinstance(result, Size)
        
    # -----------------------------------
    # Test boolean methods
    # -----------------------------------
    
    def test_and_(self):
        """Test the and_() method of the Dollar class."""
        from monggregate.operators.boolean import And
        
        result = Dollar.and_("$a", "$b")
        assert isinstance(result, And)
        
    def test_not_(self):
        """Test the not_() method of the Dollar class."""
        from monggregate.operators.boolean import Not
        
        result = Dollar.not_("$condition")
        assert isinstance(result, Not)
        
    def test_or_(self):
        """Test the or_() method of the Dollar class."""
        from monggregate.operators.boolean import Or
        
        result = Dollar.or_("$a", "$b")
        assert isinstance(result, Or)
        
    # -----------------------------------
    # Test comparison methods
    # -----------------------------------
    
    def test_cmp(self):
        """Test the cmp() method of the Dollar class."""
        from monggregate.operators.comparison import Cmp
        
        result = Dollar.cmp("$a", "$b")
        assert isinstance(result, Cmp)
        
    def test_eq(self):
        """Test the eq() method of the Dollar class."""
        from monggregate.operators.comparison import Eq
        
        result = Dollar.eq("$a", "$b")
        assert isinstance(result, Eq)
        
    def test_gt(self):
        """Test the gt() method of the Dollar class."""
        from monggregate.operators.comparison import Gt
        
        result = Dollar.gt("$a", "$b")
        assert isinstance(result, Gt)
        
    def test_gte(self):
        """Test the gte() method of the Dollar class."""
        from monggregate.operators.comparison import Gte
        
        result = Dollar.gte("$a", "$b")
        assert isinstance(result, Gte)
        
    def test_lt(self):
        """Test the lt() method of the Dollar class."""
        from monggregate.operators.comparison import Lt
        
        result = Dollar.lt("$a", "$b")
        assert isinstance(result, Lt)
        
    def test_lte(self):
        """Test the lte() method of the Dollar class."""
        from monggregate.operators.comparison import Lte
        
        result = Dollar.lte("$a", "$b")
        assert isinstance(result, Lte)
        
    def test_ne(self):
        """Test the ne() method of the Dollar class."""
        from monggregate.operators.comparison import Ne
        
        result = Dollar.ne("$a", "$b")
        assert isinstance(result, Ne)
        
    # -----------------------------------
    # Test conditional methods
    # -----------------------------------
    
    def test_if_null(self):
        """Test the if_null() method of the Dollar class."""
        from monggregate.operators.conditional import IfNull
        
        result = Dollar.if_null("$field", "default")
        assert isinstance(result, IfNull)
        
    def test_switch(self):
        """Test the switch() method of the Dollar class."""
        from monggregate.operators.conditional import Switch
        
        branches = [{"case": {"$eq": ["$grade", "A"]}, "then": "Excellent"}]
        result = Dollar.switch(branches=branches, default="Unknown")
        assert isinstance(result, Switch)
        
    # -----------------------------------
    # Test string methods
    # -----------------------------------
    
    def test_concat(self):
        """Test the concat() method of the Dollar class."""
        from monggregate.operators.strings import Concat
        
        result = Dollar.concat("$first", " ", "$last")
        assert isinstance(result, Concat)
        
    def test_date_from_string(self):
        """Test the date_from_string() method of the Dollar class."""
        from monggregate.operators.strings import DateFromString
        
        result = Dollar.date_from_string(date_string="$dateString")
        assert isinstance(result, DateFromString)
        
    def test_date_to_string(self):
        """Test the date_to_string() method of the Dollar class."""
        from monggregate.operators.strings import DateToString
        
        # Check the actual signature of date_to_string method
        result = Dollar.date_to_string("$date", "%Y-%m-%d")
        assert isinstance(result, DateToString)
        
    # -----------------------------------
    # Test object methods
    # -----------------------------------
    
    def test_merge_objects(self):
        """Test the merge_objects() method of the Dollar class."""
        from monggregate.operators.objects import MergeObjects
        
        # merge_objects takes a single operand (array of objects)
        result = Dollar.merge_objects(["$obj1", "$obj2"])
        assert isinstance(result, MergeObjects)
        
    def test_object_to_array(self):
        """Test the object_to_array() method of the Dollar class."""
        from monggregate.operators.objects import ObjectToArray
        
        result = Dollar.object_to_array("$object")
        assert isinstance(result, ObjectToArray)
        
    # -----------------------------------
    # Test type methods
    # -----------------------------------
    
    def test_type_(self):
        """Test the type_() method of the Dollar class."""
        from monggregate.operators.type_.type_ import Type_
        
        result = Dollar.type_("$field")
        assert isinstance(result, Type_)


class TestDollarDollar:
    """Test the DollarDollar class."""

    def test_instantiation(self):
        """Test that DollarDollar class can be accessed correctly and returns dollar-prefixed fields."""

        dollar_dollar = DollarDollar()
        assert isinstance(dollar_dollar, DollarDollar)

    def test____getattr__(self):
        """Test the __getattr__ method of the DollarDollar class."""

        assert DollarDollar().name == "$$name"

    def test_singleton(self):
        """Test that DollarDollar class is a singleton."""

        assert DollarDollar() is DollarDollar()
        assert DollarDollar() is SS

    def test_constants_access(self):
        """Test accessing constants from DollarDollar class."""

        # Test accessing constants
        assert DollarDollar().ROOT == "$$ROOT"
        assert DollarDollar().CURRENT == "$$CURRENT"
        assert DollarDollar().NOW == "$$NOW"
