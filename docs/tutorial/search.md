# Atlas Search in Monggregate

MongoDB's aggregation framework provides powerful search capabilities through the `$search` and `$searchMeta` stages, available exclusively with MongoDB Atlas. Monggregate makes these advanced search features accessible through an intuitive Python interface.

## What is Atlas Search?

Atlas Search integrates full-text search capabilities directly into your MongoDB database, providing functionality similar to dedicated search engines like Elasticsearch or Algolia:

- **Full-text search** with language-aware text analysis
- **Fuzzy matching** to handle typos and misspellings
- **Autocomplete** suggestions for partial queries
- **Relevance scoring** to rank results by importance
- **Highlighting** to emphasize matching terms
- **Faceting** for categorizing and filtering results
- **Geospatial search** for location-based queries
- **Vector search** for semantic similarity and AI applications

For a complete feature list, see the [Atlas Search documentation](https://www.mongodb.com/docs/atlas/atlas-search/atlas-search-overview/).

## Basic Search Queries

Creating a basic search query with Monggregate is straightforward:

```python
from monggregate import Pipeline

pipeline = Pipeline()
pipeline.search(
    path="description",  # Field to search in
    query="apple"        # Search term
)
```

By default, Monggregate uses the `text` operator for search queries. This query will find all documents containing "apple" in the description field.

### Adding Fuzzy Matching

To handle typos and minor spelling variations, add fuzzy matching:

```python
from monggregate import Pipeline
from monggregate.search.commons import FuzzyOptions

pipeline = Pipeline()
pipeline.search(
    path="description",
    query="apple",
    fuzzy=FuzzyOptions(
        max_edits=2  # Allow up to 2 character edits
    )
)
```

This query will match terms like "appl", "appel", or "aple" in addition to "apple".

## Advanced Search with Operators

Atlas Search provides several specialized operators for different search needs:

### Text Search

```python
pipeline = Pipeline()
pipeline.search(
    operator_name="text",  # Explicitly specify text operator
    path="plot",
    query="space adventure",
    fuzzy=FuzzyOptions(max_edits=1)
)
```

### Autocomplete

```python
pipeline = Pipeline()
pipeline.search(
    operator_name="autocomplete",
    path="title",
    query="star w",      # Will match "Star Wars"
    fuzzy=FuzzyOptions(max_edits=1)
)
```

### Regex Search

```python
pipeline = Pipeline()
pipeline.search(
    operator_name="regex",
    path="email",
    query="^john\\.[a-z]+@example\\.com$"  # Match specific email pattern
)
```

## Compound Search Queries

The real power of Atlas Search emerges with compound queries that combine multiple search conditions. The `compound` operator supports four types of clauses:

- **must**: Documents MUST match these conditions AND they affect relevance score
- **filter**: Documents MUST match these conditions but they DON'T affect relevance score
- **should**: Documents SHOULD match these conditions and they affect relevance score
- **mustNot**: Documents MUST NOT match these conditions

### Building Compound Queries

Monggregate provides a unique "search pipeline" approach for building compound queries:

```python
pipeline = Pipeline()
# Initialize a compound search
pipeline.search(
    index="movies",           # Search index name
    operator_name="compound"
).search(                     # Add a "must" clause
    clause_type="must", 
    query="adventure",
    path="genres"
).search(                     # Add a "should" clause
    clause_type="should",
    query="space",
    path="plot"
).search(                     # Add a "mustNot" clause
    clause_type="mustNot",
    query="horror",
    path="genres"
)
```

This query will:
1. REQUIRE documents to have "adventure" in the genres field
2. PREFER documents with "space" in the plot (boosting relevance score)
3. EXCLUDE documents with "horror" in the genres field

The resulting MongoDB aggregation will look like:

```json
[
    {
        "$search": {
            "index": "movies",
            "compound": {
                "must": {
                    "text": {
                        "query": "adventure",
                        "path": "genres"
                    }
                },
                "should": {
                    "text": {
                        "query": "space",
                        "path": "plot"
                    }
                },
                "mustNot": {
                    "text": {
                        "query": "horror",
                        "path": "genres"
                    }
                }
            }
        }
    }
]
```

## Faceted Search with searchMeta

Faceted search allows users to filter and navigate search results by categories or attributes. Use the `search_meta` stage to implement faceting:

```python
pipeline = Pipeline()
# Initialize a faceted search
pipeline.search_meta(
    index="movies",
    collector_name="facet"
).search_meta(               # Add string facet on genres
    facet_type="string",
    path="genres",
    num_buckets=10           # Return top 10 genres
).search_meta(               # Add numeric facet on year
    facet_type="number",
    path="year",
    boundaries=[1970, 1980, 1990, 2000, 2010, 2020]
)
```

This creates a faceted search that:
1. Groups movies by genre, showing the top 10 most common genres
2. Splits movies into date ranges (pre-1970, 1970s, 1980s, etc.)

### Combining Search and Facets

You can combine regular search with faceting to create powerful filtered search experiences:

```python
pipeline = Pipeline()
# First define search criteria
pipeline.search_meta(
    index="movies",
    operator_name="text",
    path="plot",
    query="space"
# Then add faceting
).search_meta(
    collector_name="facet"
).search_meta(
    facet_type="string",
    path="genres"
)
```

This will search for "space" in movie plots, then return facet counts showing which genres are most common in the results.

## Complete Search Example

Here's a comprehensive example that combines multiple search features:

```python
# Create search pipeline
pipeline = Pipeline()
pipeline.search(
    index="default",
    operator_name="compound"
).search(
    # Movies must be from the 2000s
    clause_type="filter",
    operator_name="range",
    path="year",
    gte=2000,
    lte=2009
).search(
    # Movies should contain "future" in plot
    clause_type="should",
    operator_name="text",
    path="plot",
    query="future",
    score={"boost": {"value": 3}}  # Boost relevance
).search(
    # Movies should contain "technology" in plot
    clause_type="should",
    operator_name="text",
    path="plot",
    query="technology"
).limit(10).project(
    title=1,
    year=1,
    plot=1,
    score={"$meta": "searchScore"}  # Include relevance score
)

# Execute the pipeline
results = list(db.movies.aggregate(pipeline.export()))
for movie in results:
    print(f"{movie['title']} ({movie['year']}) - Score: {movie['score']:.2f}")
```

## Next Steps

- Learn about [vector search capabilities](vector-search.md) for semantic search and AI applications
- Explore the full range of [MongoDB operators](operators.md) for additional data manipulation
- Understand how to build complex [aggregation pipelines](pipeline.md) combining search with other stages
