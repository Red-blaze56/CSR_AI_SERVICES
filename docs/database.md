# Database Schema

The CSR AI service uses Supabase with pgvector for vector search.

---

## campaigns

Stores generated CSR campaign data.

```sql
CREATE TABLE campaigns (
  id UUID PRIMARY KEY,
  company_id INTEGER,
  cause TEXT,
  region TEXT,
  budget_inr NUMERIC,
  timeline INTEGER,
  title TEXT,
  description TEXT,
  budget_breakdown JSONB,
  schedule_vii TEXT,
  sdg_alignment INTEGER[],
  impact_metrics JSONB,
  milestones JSONB,
  created_at TIMESTAMPTZ
);
```

---

## campaign_embeddings

Stores vector embeddings used for RAG retrieval.

```sql
CREATE TABLE campaign_embeddings (
  id UUID PRIMARY KEY,
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  embedding VECTOR(384),
  metadata JSONB,
  version INTEGER,
  created_at TIMESTAMPTZ
);
```

---

## Vector Index

The system uses HNSW indexing for fast similarity search.

```sql
CREATE INDEX campaign_embeddings_embedding_idx
ON campaign_embeddings
USING hnsw (embedding vector_cosine_ops);
```

---

## Vector Search Function

```
match_campaigns(query_embedding, match_threshold, match_count)
```

Used to retrieve similar campaigns from the vector database.

---

## RAG Retrieval Process

1. Generate embedding from user request.
2. Call `match_campaigns`.
3. Retrieve similar campaigns.
4. Use retrieved campaigns as context for generation.
