# SECE — Smart Evidence Correlation Engine

An AI-assisted digital forensics and investigation web platform designed to automate heterogeneous evidence triage, extract forensic entities, verify file integrity, and discover correlation chains across disparate evidence sources.

---

## 📌 Project Overview
Digital investigations routinely produce disconnected evidence items (email dumps, call records, chat exports, transaction ledgers). Investigators traditionally analyze these files manually to identify overlapping leads.

**SECE** automates this workflow:
1. Ingests heterogeneous evidence files preserving original custody.
2. Calculates an immutable **SHA-256** integrity fingerprint upon upload.
3. Modularly parses technical metadata and text content.
4. Extracts deterministic indicators (Email, IP, Phone) via regex and entities (Person, Location) via NLP.
5. Runs a **Cross-Evidence Correlation Engine** to identify candidate linkages and relationships between separate evidence sources.
6. Presents findings in an investigation dashboard with complete chain-of-custody audit logs.

---

## 🛠️ Technology Stack
* **Backend Framework**: FastAPI (Python 3.14)
* **Database & Persistence**: PostgreSQL 18.6 with SQLAlchemy ORM
* **Authentication**: JWT (JSON Web Tokens) with Passlib & Bcrypt password hashing
* **Parsing Engine**: Modular Factory (`.txt`, `.csv`, `.pdf` via `pypdf`)
* **Entity Extraction**: High-precision Regex + Named Entity Recognition (NER)
* **Frontend**: HTML5, Modern CSS, Vanilla JavaScript, Jinja2 Templates

---

## 📂 Mini Project Scope (Modules 1–7)
* **Module 1**: Authentication & User Management (Role-based access control, JWT)
* **Module 2**: Case / Investigation Management (CRUD operations, status lifecycles, audit triggers)
* **Module 3**: Evidence Upload & Integrity Verification (Streaming SHA-256, path traversal protection)
* **Module 4**: Metadata & Content Extraction (Factory parsers for text, CSV, PDF, JSONB metadata)
* **Module 5**: Entity Extraction & Normalization (Regex, NLP, offset tracking, canonical identities)
* **Module 6**: Cross-Evidence Correlation Engine (Candidate matching, confidence scoring, link discovery)
* **Module 7**: Investigation Dashboard & Summary View (Metrics, evidence ledger, correlation view, audit trails)

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
* Python 3.10+
* PostgreSQL 18.x installed and running on port 5432

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone [https://github.com/SubhaMariappan/Smart-Evidence-Correlation-Engine.git](https://github.com/SubhaMariappan/Smart-Evidence-Correlation-Engine.git)
cd Smart-Evidence-Correlation-Engine
python -m venv .venv
.\.venv\Scripts\activate   # Windows
