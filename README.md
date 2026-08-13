# Enterprise AI Data Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Microsoft Azure](https://img.shields.io/badge/Cloud-Azure-0078D4)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

A cloud-native **Data Engineering + Generative AI** platform built on Microsoft Azure. It pulls data in from multiple sources, cleans and organizes it, stores it in a data lake, and lets users ask natural-language questions about their documents using **Retrieval-Augmented Generation (RAG)**.

In short: it automates the boring parts of moving and cleaning enterprise data, and adds an AI chat layer on top so people can "talk to their data."

---

## Table of Contents

- [Project Goals](#project-goals)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Testing](#testing)
- [Monitoring](#monitoring)
- [Security](#security)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Project Goals

- Build a scalable data lake on Azure
- Automate data ingestion and ETL (Extract, Transform, Load) pipelines
- Improve data quality through validation checks
- Track metadata and pipeline execution history
- Enable semantic (meaning-based) search using Generative AI
- Monitor pipeline health and catch failures early
- Demonstrate production-ready Data Engineering practices

---

## Features

### Data Ingestion
Bring data in from wherever it lives:
- CSV files
- REST APIs
- Relational databases
- PDF documents
- Incremental loading (only pulls new/changed data instead of reloading everything)

### Data Engineering
- ETL pipelines (Extract → Transform → Load)
- Data validation and quality checks
- Schema management (keeping data structure consistent)
- Metadata tracking and data lineage (knowing where data came from and how it changed)
- Data partitioning for faster queries

### Generative AI (RAG)
- OCR (text extraction from scanned documents)
- Document parsing
- Embedding generation (turning text into AI-searchable vectors)
- Vector database storage (Azure AI Search / Weaviate)
- Semantic search
- AI-powered question answering over your own documents

### Monitoring
- Pipeline health dashboard
- Azure Monitor metrics and logs
- Alerts via Azure Service Bus
- Data freshness tracking

---

## Architecture

```
                        +----------------------+
                        | Enterprise Data      |
                        | Sources              |
                        +----------+-----------+
                                   |
          --------------------------------------------------
          |                 |              |               |
        CSV Files        REST APIs      Databases        PDF Files
          |                 |              |               |
          --------------------------------------------------
                                   |
                                   v
                    Data Ingestion Pipeline (Python)
                                   |
                                   v
                      Data Validation & Cleaning
                                   |
                                   v
                    Azure Data Lake Storage (ADLS)
                                   |
                    +--------------+--------------+
                    |                             |
                    v                             v
           Metadata Catalog              ETL Processing
                    |                             |
                    +--------------+--------------+
                                   |
                                   v
                           Analytics Layer
                                   |
                                   v
                        Embedding Generation
                                   |
                                   v
                        Vector Database
                                   |
                                   v
                      GenAI RAG Chat Assistant
```

**In plain terms:** raw data comes in from four sources → gets cleaned and checked → lands in Azure Data Lake Storage → gets cataloged and processed → feeds both a regular analytics layer and an AI pipeline that turns documents into searchable embeddings → users can then chat with an AI assistant that answers questions using that data.

> A rendered version of this diagram lives at `architecture/architecture.png`.

---

## Project Structure

```
enterprise-ai-data-platform/
│
├── architecture/           # Diagrams and data-flow documentation
│   ├── architecture.png
│   └── data_flow.md
│
├── ingestion/               # Code that pulls data in from each source
│   ├── csv_loader.py
│   ├── api_loader.py
│   ├── database_loader.py
│   └── pdf_loader.py
│
├── pipelines/                # ETL, validation, and metadata logic
│   ├── etl_pipeline.py
│   ├── incremental_load.py
│   ├── data_validation.py
│   ├── schema_manager.py
│   └── metadata_catalog.py
│
├── storage/                  # Azure Data Lake read/write and partitioning
│   ├── adls_manager.py
│   └── partition_manager.py
│
├── genai/                    # RAG / AI chat pipeline
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── rag_pipeline.py
│   └── llm_chat.py
│
├── monitoring/                # Health checks, alerts, dashboards
│   ├── azure_monitor.py
│   ├── alerting.py
│   └── dashboard.py
│
├── infrastructure/
│   └── terraform/             # Infrastructure as Code (Azure resources)
│
├── tests/                     # Unit and integration tests
│
├── README.md
├── requirements.txt
└── .env.example                # Template for required environment variables
```

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.x |
| Backend / API | FastAPI |
| Databases | Azure SQL Database, MySQL |
| Data Engineering | Pandas, Polars, PyArrow, SQLAlchemy |
| Cloud (Azure) | ADLS, Azure Functions, Azure Monitor, Service Bus, Azure IAM, Key Vault, Event Grid |
| AI / GenAI | LangChain, Azure OpenAI / Google Gemini, Azure AI Search, Sentence Transformers |
| DevOps | Docker, Terraform, GitHub Actions |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- An Azure account with access to: Data Lake Storage, Azure SQL (or MySQL), Key Vault, and Azure OpenAI (or a Google Gemini API key)
- Docker (optional, for containerized runs)
- Terraform (optional, only if you plan to provision Azure infrastructure yourself)

### 1. Clone the repository

```bash
git clone https://github.com/Sairaj-25/enterprise-ai-data-platform.git
cd enterprise-ai-data-platform
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and fill in your own credentials:

```bash
cp .env.example .env
```

Typical variables you'll need to set (match these to your actual `.env.example`):

| Variable | Purpose |
|---|---|
| `AZURE_STORAGE_CONNECTION_STRING` | Connects to Azure Data Lake Storage |
| `AZURE_SQL_CONNECTION_STRING` | Connects to Azure SQL / MySQL |
| `AZURE_OPENAI_API_KEY` | Used for embeddings and the chat assistant |
| `AZURE_KEY_VAULT_URL` | Retrieves secrets securely |
| `VECTOR_DB_API_KEY` | Connects to Azure AI Search / Weaviate |

> Never commit your `.env` file. It's already excluded via `.gitignore`.

### 4. Run a pipeline

```bash
python pipelines/etl_pipeline.py
```

### 5. Start the API server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Usage

Once the server is running, you can query the RAG chat assistant, for example:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What were last quarter's sales figures?"}'
```

The assistant retrieves relevant chunks from the vector database and uses the LLM to generate an answer grounded in your ingested documents.

---

## Testing

Run the test suite with:

```bash
pytest tests/
```

---

## Monitoring

The platform continuously tracks:

- Pipeline execution and failed jobs
- Data freshness and quality
- Storage usage
- API failures
- AI request metrics

Alerts are pushed through Azure Service Bus, and metrics/logs are visible in Azure Monitor.

---

## Security

- Azure IAM with least-privilege access
- Encryption at rest and in transit
- Secrets stored in Azure Key Vault (no hardcoded credentials)
- Managed Identities for service-to-service auth
- Secure API authentication

---

## Roadmap

Planned or potential future additions:

- Azure Data Factory for orchestration
- Apache Spark support via Synapse Analytics
- Streaming with Kafka / Azure Event Hubs
- Apache Iceberg / Apache Hive support
- Azure Purview for data cataloging
- Full Azure Synapse Analytics integration
- ML model monitoring with Azure ML
- Multi-region deployment

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Push to your branch and open a Pull Request

Please open an issue first for major changes so they can be discussed.


---

## Author

**Sairaj Jadhav**
GitHub: [https://github.com/Sairaj-25](https://github.com/Sairaj-25)
