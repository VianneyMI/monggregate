"""Tests for `monggregate.search.collectors.facet` module."""

import pytest
from datetime import datetime

from monggregate.search.collectors.facet import (
    Facet, FacetName, FacetBucket, FacetBuckets, 
    StringFacet, NumericFacet, DateFacet
)


class TestFacetName:
    """Tests for the `FacetName` class."""

    def test_is_subclass_of_field_name(self) -> None:
        """Test that `FacetName` is a subclass of `FieldName`."""
        from monggregate.fields import FieldName

        assert issubclass(FacetName, FieldName)


class TestFacetBucket:
    """Tests for the `FacetBucket` class."""

    @pytest.mark.xfail(
        reason="Pydantic v1 ignore fields starting with _. Will be fixed in Pydantic v2 or by config."
    )
    def test_has_required_fields(self) -> None:
        """Test that `FacetBucket` has the required fields."""
        bucket = FacetBucket(_id="test", count=1)
        assert bucket._id == "test"
        assert bucket.count == 1

    def test_expression_property(self) -> None:
        """Test that `expression` property returns model dump."""
        bucket = FacetBucket(_id="test", count=5)
        expression = bucket.expression
        assert isinstance(expression, dict)
        assert expression["count"] == 5


class TestFacetBuckets:
    """Tests for the `FacetBuckets` class."""

    def test_creation_with_buckets(self) -> None:
        """Test creating FacetBuckets with a list of buckets."""
        bucket1 = FacetBucket(_id="value1", count=10)
        bucket2 = FacetBucket(_id="value2", count=5)
        buckets = FacetBuckets(buckets=[bucket1, bucket2])
        
        assert len(buckets.buckets) == 2
        assert buckets.buckets[0].count == 10
        assert buckets.buckets[1].count == 5

    def test_expression_property(self) -> None:
        """Test that `expression` property returns model dump."""
        bucket = FacetBucket(_id="test", count=5)
        buckets = FacetBuckets(buckets=[bucket])
        expression = buckets.expression
        assert isinstance(expression, dict)
        assert "buckets" in expression


class TestStringFacet:
    """Tests for the `StringFacet` class."""

    def test_creation_with_defaults(self) -> None:
        """Test creating StringFacet with default values."""
        facet = StringFacet(path="category")
        assert facet.path == "category"
        assert facet.name == "category"  # Should default to path
        assert facet.type == "string"
        assert facet.num_buckets == 10

    def test_creation_with_custom_values(self) -> None:
        """Test creating StringFacet with custom values."""
        facet = StringFacet(path="category", name="custom_name", num_buckets=20)
        assert facet.path == "category"
        assert facet.name == "custom_name"
        assert facet.num_buckets == 20

    def test_expression_property(self) -> None:
        """Test that `expression` property returns correct format."""
        facet = StringFacet(path="category", name="cat_facet", num_buckets=15)
        expression = facet.expression
        assert isinstance(expression, dict)
        assert "cat_facet" in expression


class TestNumericFacet:
    """Tests for the `NumericFacet` class."""

    def test_creation_with_boundaries(self) -> None:
        """Test creating NumericFacet with boundaries."""
        boundaries = [0, 10, 20, 30]
        facet = NumericFacet(path="price", boundaries=boundaries, default="other")
        assert facet.path == "price"
        assert facet.name == "price"
        assert facet.type == "number"
        assert facet.boundaries == boundaries
        assert facet.default == "other"

    def test_expression_property(self) -> None:
        """Test that `expression` property returns correct format."""
        boundaries = [0, 100, 200]
        facet = NumericFacet(path="price", boundaries=boundaries)
        expression = facet.expression
        assert isinstance(expression, dict)
        assert "price" in expression


class TestDateFacet:
    """Tests for the `DateFacet` class."""

    def test_creation_with_boundaries(self) -> None:
        """Test creating DateFacet with boundaries."""
        boundaries = [
            datetime(2023, 1, 1),
            datetime(2023, 6, 1),
            datetime(2024, 1, 1)
        ]
        facet = DateFacet(path="created_at", boundaries=boundaries, default="other")
        assert facet.path == "created_at"
        assert facet.name == "created_at"
        assert facet.type == "date"
        assert facet.boundaries == boundaries
        assert facet.default == "other"

    def test_expression_property(self) -> None:
        """Test that `expression` property returns correct format."""
        boundaries = [datetime(2023, 1, 1), datetime(2024, 1, 1)]
        facet = DateFacet(path="created_at", boundaries=boundaries)
        expression = facet.expression
        assert isinstance(expression, dict)
        assert "created_at" in expression


class TestFacet:
    """Tests for the `Facet` class."""

    def test_is_subclass_of_search_collector(self) -> None:
        """Test that `Facet` is a subclass of `SearchCollector`."""
        from monggregate.search.collectors.collector import SearchCollector

        assert issubclass(Facet, SearchCollector)

    def test_init_autocomplete(self) -> None:
        """Test that `init_autocomplete` creates a facet with an autocomplete operator."""
        from monggregate.search.operators import Autocomplete

        facet = Facet.init_autocomplete(query="test", path="field")
        assert isinstance(facet.operator, Autocomplete)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_text(self) -> None:
        """Test that `init_text` creates a facet with a text operator."""
        from monggregate.search.operators import Text

        facet = Facet.init_text(query="test", path="field")
        assert isinstance(facet.operator, Text)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_regex(self) -> None:
        """Test that `init_regex` creates a facet with a regex operator."""
        from monggregate.search.operators import Regex

        facet = Facet.init_regex(query="test", path="field")
        assert isinstance(facet.operator, Regex)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_wildcard(self) -> None:
        """Test that `init_wildcard` creates a facet with a wildcard operator."""
        from monggregate.search.operators import Wildcard

        facet = Facet.init_wildcard(query="test", path="field")
        assert isinstance(facet.operator, Wildcard)
        assert facet.operator.query == "test"
        assert facet.operator.path == "field"

    def test_init_compound(self) -> None:
        """Test that `init_compound` creates a facet with a compound operator."""
        from monggregate.search.operators import Compound, Text

        text_op = Text(query="test", path="field")
        facet = Facet.init_compound(must=[text_op], minimum_should_clause=1)
        assert isinstance(facet.operator, Compound)
        assert len(facet.operator.must) == 1

    def test_init_equals(self) -> None:
        """Test that `init_equals` creates a facet with an equals operator."""
        from monggregate.search.operators import Equals

        facet = Facet.init_equals(path="status", value="active")
        assert isinstance(facet.operator, Equals)
        assert facet.operator.path == "status"
        assert facet.operator.value == "active"

    def test_init_exists(self) -> None:
        """Test that `init_exists` creates a facet with an exists operator."""
        from monggregate.search.operators import Exists

        facet = Facet.init_exists(path="field")
        assert isinstance(facet.operator, Exists)
        assert facet.operator.path == "field"

    def test_init_more_like_this(self) -> None:
        """Test that `init_more_like_this` creates a facet with a more_like_this operator."""
        from monggregate.search.operators import MoreLikeThis

        like_doc = {"title": "test document"}
        facet = Facet.init_more_like_this(like=like_doc)
        assert isinstance(facet.operator, MoreLikeThis)
        assert facet.operator.like == like_doc

    def test_init_range(self) -> None:
        """Test that `init_range` creates a facet with a range operator."""
        from monggregate.search.operators import Range

        facet = Facet.init_range(path="price", gte=10, lte=100)
        assert isinstance(facet.operator, Range)
        assert facet.operator.path == "price"
        assert facet.operator.gte == 10
        assert facet.operator.lte == 100

    def test_from_operator(self) -> None:
        """Test that `from_operator` creates a facet from operator name."""
        facet = Facet.from_operator("text", query="test", path="field")
        from monggregate.search.operators import Text
        assert isinstance(facet.operator, Text)

    def test_validate_facets_unique_names(self) -> None:
        """Test that facets validation ensures unique names."""
        facet1 = StringFacet(path="category", name="cat")
        facet2 = StringFacet(path="type", name="cat")  # Same name
        
        with pytest.raises(ValueError, match="Some facets have identical names"):
            Facet(facets=[facet1, facet2])

    def test_expression_with_no_facets_raises_error(self) -> None:
        """Test that expression raises error when no facets are defined."""
        facet = Facet()
        with pytest.raises(ValueError, match="No facets were defined"):
            _ = facet.expression

    def test_expression_with_facets_and_operator(self) -> None:
        """Test that expression works with facets and operator."""
        from monggregate.search.operators import Text
        
        string_facet = StringFacet(path="category")
        text_op = Text(query="test", path="title")
        facet = Facet(operator=text_op, facets=[string_facet])
        
        expression = facet.expression
        assert "facet" in expression
        assert "facets" in expression["facet"]
        assert "operator" in expression["facet"]

    def test_expression_with_facets_only(self) -> None:
        """Test that expression works with facets but no operator."""
        string_facet = StringFacet(path="category")
        facet = Facet(facets=[string_facet])
        
        expression = facet.expression
        assert "facet" in expression
        assert "facets" in expression["facet"]
        assert "operator" not in expression["facet"]

    def test_autocomplete_method_with_no_existing_operator(self) -> None:
        """Test autocomplete method when no operator exists."""
        facet = Facet()
        result = facet.autocomplete(query="test", path="field")
        
        assert result is facet  # Should return self
        from monggregate.search.operators import Autocomplete
        assert isinstance(facet.operator, Autocomplete)

    def test_autocomplete_method_with_compound_operator(self) -> None:
        """Test autocomplete method when compound operator exists."""
        from monggregate.search.operators import Compound, Text
        
        text_op = Text(query="existing", path="field1")
        compound_op = Compound(should=[text_op])
        facet = Facet(operator=compound_op)
        
        result = facet.autocomplete(query="test", path="field2")
        assert result is facet
        assert isinstance(facet.operator, Compound)

    def test_autocomplete_method_with_simple_operator(self) -> None:
        """Test autocomplete method when simple operator exists."""
        from monggregate.search.operators import Text, Compound
        
        text_op = Text(query="existing", path="field1")
        facet = Facet(operator=text_op)
        
        result = facet.autocomplete(query="test", path="field2")
        assert result is facet
        assert isinstance(facet.operator, Compound)

    def test_equals_method_with_no_existing_operator(self) -> None:
        """Test equals method when no operator exists."""
        facet = Facet()
        result = facet.equals(path="status", value="active")
        
        assert result is facet
        from monggregate.search.operators import Equals
        assert isinstance(facet.operator, Equals)

    def test_exists_method_with_no_existing_operator(self) -> None:
        """Test exists method when no operator exists."""
        facet = Facet()
        result = facet.exists(path="field")
        
        assert result is facet
        from monggregate.search.operators import Exists
        assert isinstance(facet.operator, Exists)

    def test_more_like_this_method_with_no_existing_operator(self) -> None:
        """Test more_like_this method when no operator exists."""
        facet = Facet()
        like_doc = {"title": "test"}
        result = facet.more_like_this(like=like_doc)
        
        assert result is facet
        from monggregate.search.operators import MoreLikeThis
        assert isinstance(facet.operator, MoreLikeThis)

    def test_range_method_with_no_existing_operator(self) -> None:
        """Test range method when no operator exists."""
        facet = Facet()
        result = facet.range(path="price", gte=10, lte=100)
        
        assert result is facet
        from monggregate.search.operators import Range
        assert isinstance(facet.operator, Range)

    def test_regex_method_with_no_existing_operator(self) -> None:
        """Test regex method when no operator exists."""
        facet = Facet()
        result = facet.regex(query="test.*", path="field")
        
        assert result is facet
        from monggregate.search.operators import Regex
        assert isinstance(facet.operator, Regex)

    def test_text_method_with_no_existing_operator(self) -> None:
        """Test text method when no operator exists."""
        facet = Facet()
        result = facet.text(query="test", path="field")
        
        assert result is facet
        from monggregate.search.operators import Text
        assert isinstance(facet.operator, Text)

    def test_wildcard_method_with_no_existing_operator(self) -> None:
        """Test wildcard method when no operator exists."""
        facet = Facet()
        result = facet.wildcard(query="test*", path="field")
        
        assert result is facet
        from monggregate.search.operators import Wildcard
        assert isinstance(facet.operator, Wildcard)

    def test_facet_method_string_type(self) -> None:
        """Test facet method with string type."""
        facet = Facet()
        result = facet.facet(path="category", type="string", num_buckets=15)
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], StringFacet)
        assert facet.facets[0].num_buckets == 15

    def test_facet_method_number_type(self) -> None:
        """Test facet method with number type."""
        facet = Facet()
        boundaries = [0, 10, 20]
        result = facet.facet(path="price", type="number", boundaries=boundaries, default="other")
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], NumericFacet)
        assert facet.facets[0].boundaries == boundaries

    def test_facet_method_date_type(self) -> None:
        """Test facet method with date type."""
        facet = Facet()
        boundaries = [datetime(2023, 1, 1), datetime(2024, 1, 1)]
        result = facet.facet(path="created_at", type="date", boundaries=boundaries)
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], DateFacet)
        assert facet.facets[0].boundaries == boundaries

    def test_facet_method_invalid_type(self) -> None:
        """Test facet method with invalid type raises error."""
        facet = Facet()
        with pytest.raises(ValueError, match="Invalid facet type"):
            facet.facet(path="field", type="invalid")

    def test_numeric_method(self) -> None:
        """Test numeric method."""
        facet = Facet()
        boundaries = [0, 10, 20]
        result = facet.numeric(path="price", boundaries=boundaries, default="other")
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], NumericFacet)

    def test_date_method(self) -> None:
        """Test date method."""
        facet = Facet()
        boundaries = [datetime(2023, 1, 1), datetime(2024, 1, 1)]
        result = facet.date(path="created_at", boundaries=boundaries)
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], DateFacet)

    def test_string_method(self) -> None:
        """Test string method."""
        facet = Facet()
        result = facet.string(path="category", num_buckets=20)
        
        assert result is facet
        assert len(facet.facets) == 1
        assert isinstance(facet.facets[0], StringFacet)
        assert facet.facets[0].num_buckets == 20

    def test_static_numeric_facet(self) -> None:
        """Test static NumericFacet method."""
        boundaries = [0, 10, 20]
        facet = Facet.NumericFacet(path="price", boundaries=boundaries, default="other")
        
        assert isinstance(facet, NumericFacet)
        assert facet.path == "price"
        assert facet.boundaries == boundaries
        assert facet.default == "other"

    def test_static_string_facet(self) -> None:
        """Test static StringFacet method."""
        facet = Facet.StringFacet(path="category", num_buckets=15)
        
        assert isinstance(facet, StringFacet)
        assert facet.path == "category"
        assert facet.num_buckets == 15

    def test_static_date_facet(self) -> None:
        """Test static DateFacet method."""
        boundaries = [datetime(2023, 1, 1), datetime(2024, 1, 1)]
        facet = Facet.DateFacet(path="created_at", boundaries=boundaries)
        
        assert isinstance(facet, DateFacet)
        assert facet.path == "created_at"
        assert facet.boundaries == boundaries

    def test_static_facet_string_type(self) -> None:
        """Test static Facet method with string type."""
        facet = Facet.Facet(type="string", path="category", num_buckets=15)
        
        assert isinstance(facet, StringFacet)
        assert facet.num_buckets == 15

    def test_static_facet_number_type(self) -> None:
        """Test static Facet method with number type."""
        boundaries = [0, 10, 20]
        facet = Facet.Facet(type="number", path="price", boundaries=boundaries)
        
        assert isinstance(facet, NumericFacet)
        assert facet.boundaries == boundaries

    def test_static_facet_date_type(self) -> None:
        """Test static Facet method with date type."""
        boundaries = [datetime(2023, 1, 1), datetime(2024, 1, 1)]
        facet = Facet.Facet(type="date", path="created_at", boundaries=boundaries)
        
        assert isinstance(facet, DateFacet)
        assert facet.boundaries == boundaries

    def test_get_constructors_map(self) -> None:
        """Test __get_constructors_map__ method."""
        # Access the private method correctly
        constructor = Facet.__get_constructors_map__("text")
        assert constructor == Facet.init_text
        
        constructor = Facet.__get_constructors_map__("autocomplete")
        assert constructor == Facet.init_autocomplete
