# 🔍 **Vector Search with Monggregate**

MongoDB Atlas provides powerful vector search capabilities through the `$vectorSearch` stage, enabling approximate nearest neighbor (aNN) search on vector embeddings. Monggregate makes these advanced vector search features accessible through an intuitive Python interface.

## 📋 **What is Vector Search?**

> 💡 Vector search allows you to find documents with similar vector embeddings to a query vector, enabling semantic search, recommendations, and AI-powered applications.

Atlas Vector Search offers:

- 🧠 **Semantic similarity** search using vector embeddings
- 🔍 **Approximate nearest neighbor** (aNN) algorithms for efficient vector comparison
- ⚡ **Fast retrieval** of similar items from large collections
- 🧩 **Pre-filtering** to narrow search scope and improve relevance
- 🔄 **Integration with AI models** like OpenAI, Hugging Face, and others

> 📚 Vector search is particularly useful for applications like:
> - Semantic text search that understands meaning, not just keywords
> - Image similarity search
> - Recommendation systems
> - AI-powered chatbots and RAG (Retrieval Augmented Generation)

## 🔰 **Prerequisites for Vector Search**

Before using vector search with Monggregate, you need to:

1. 📊 **Create an Atlas Vector Search index** on your collection
2. 🧪 **Generate vector embeddings** for your documents using an embedding model
3. 💾 **Store these embeddings** in your MongoDB documents

> ⚠️ Vector search is only available on MongoDB Atlas clusters running v6.0.11 or v7.0.2 and later.

## 🚀 **Basic Vector Search**

Creating a vector search query with Monggregate is straightforward:

```python
from monggregate import Pipeline

# Generate or obtain your query vector (embedding)
query_vector = [0.1, 0.2, 0.3, 0.4, ...]  # Your vector dimensions here

# Build the vector search pipeline
pipeline = Pipeline()
pipeline.vector_search(
    index="vector_index",        # Name of your Atlas Vector Search index
    path="embedding",            # Field containing vector embeddings
    query_vector=query_vector,   # Your search vector
    num_candidates=100,          # Number of candidates to consider
    limit=10                     # Number of results to return
)
```

> 📘 This query will find the 10 documents whose embedding vectors are most similar to your query vector, considering 100 nearest neighbors during the search.

## 🔍 **Filtering Vector Search Results**

You can narrow your vector search with filters:

```python
from monggregate import Pipeline

pipeline = Pipeline()
pipeline.vector_search(
    index="product_embeddings",
    path="product_vector",
    query_vector=query_vector,
    num_candidates=200,
    limit=20,
    filter={
        "category": "electronics",
        "price": {"$lt": 1000}
    }
)
```

> 🔍 This search will only consider products in the "electronics" category with a price less than 1000.

## 🌟 **Retrieving Search Scores**

To include the similarity score in your results:

```python
pipeline = Pipeline()
pipeline.vector_search(
    index="text_embeddings",
    path="content_vector",
    query_vector=query_vector,
    num_candidates=150,
    limit=10
).project(
    content=1,
    metadata=1,
    score={"$meta": "vectorSearchScore"}  # Include the vector similarity score
)
```

> 💯 Atlas Vector Search assigns a score between 0 and 1 to each result, with higher scores indicating greater similarity.

## 📝 **Complete Example: Semantic Search**

Here's a comprehensive example that uses vector search for a semantic search application:

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from monggregate import Pipeline
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://...")
db = client["knowledgebase"]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embedding for user query
user_query = "How do I implement authentication in my application?"
query_embedding = model.encode(user_query).tolist()

# Create vector search pipeline
pipeline = Pipeline()
pipeline.vector_search(
    index="document_vectors",
    path="embedding",
    query_vector=query_embedding,
    num_candidates=100,
    limit=5,
    filter={
        "document_type": "article",
        "status": "published"
    }
).project(
    title=1,
    content=1,
    url=1,
    score={"$meta": "vectorSearchScore"}
)

# Execute search
results = list(db.documents.aggregate(pipeline.export()))

# Display results
for doc in results:
    print(f"Title: {doc['title']}")
    print(f"Score: {doc['score']:.4f}")
    print(f"URL: {doc['url']}")
    print("-" * 40)
```

## 🔬 **Technical Details**

- 🔢 **Vector dimensions**: Your query vector must have the same number of dimensions as the vectors in your indexed field
- 🎯 **numCandidates**: Should be greater than the limit for better accuracy, typically 10-20x for optimal recall
- ⚡ **Performance tuning**: Adjust numCandidates to balance between search quality and speed
- 🔄 **Filtering**: Only works on indexed fields marked as the "filter" type in your vector search index
- 📊 **Scoring**: For cosine and dotProduct similarities, scores are normalized using the formula: `score = (1 + cosine/dot_product(v1,v2)) / 2`

## 🔜 **Next Steps**

- 🛠️ Explore the full range of [MongoDB operators](operators.md) for additional data manipulation
- 🔄 Learn how to build complex [aggregation pipelines](pipeline.md) combining vector search with other stages
- 🔍 Discover [Atlas Search capabilities](search.md) for traditional text search and faceting