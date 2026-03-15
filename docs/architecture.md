# CSR AI Service Architecture

## Overview

The CSR AI Service provides two main capabilities:

1. Conversational CSR preference collection
2. CSR campaign generation using Retrieval-Augmented Generation (RAG)

The service is implemented as an independent AI microservice and integrates with the backend through HTTP APIs.

---

## System Flow
User
↓
CSR Agent (/csr-agent/chat)
↓
Preferences Extracted
↓
Backend creates embedding
↓
Supabase Vector Search (RAG)
↓
Similar Campaigns Retrieved
↓
Campaign Generation (/generate-campaign)
↓
LLM Output
↓
Store Campaign + Embedding


---

## Components

### CSR Agent
Collects CSR campaign preferences step-by-step from the user.

Collected fields:
- budget
- cause
- region
- timeline
- employee engagement

---

### Campaign Generation
Generates structured CSR campaign proposals using Groq.

Generated fields include:

- title
- description
- budget breakdown
- milestones
- SDG alignment
- schedule VII category
- impact metrics

---

### Retrieval-Augmented Generation (RAG)

The system retrieves similar campaigns from the vector database before generation.

Steps:

1. Convert user request to embedding
2. Search vector database
3. Retrieve similar campaigns
4. Include them as context in the LLM prompt

This improves generation quality and consistency.

---

## Technologies

| Provider | Use Case | 
|----------|-------| 
| **Groq** | Primary (fast generation) | 
| **Gemini Flash** | Fallback (reasoning) | 
| **Together.ai** | Emergency fallback |

| Component | Technology |
|--------|------------|
LLM | Groq |
Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
Vector DB | Supabase pgvector |
Vector Index | HNSW |
Backend | Supabase RPC |