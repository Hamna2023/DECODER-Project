# 🧠 Mini-DECODER Prototype  
**MSc-Level Assignment — DECODER Project (Concordia University)**  
Supervisor: *Professor Yann-Gaël Guéhéneuc*

---

## 🎯 Project Overview
This prototype simulates a minimal version of the **DECODER** platform — a research project focused on reducing building-related emissions through software modeling, IoT integration, and predictive analytics.

The **Mini-DECODER** prototype demonstrates:
- Ingestion of simulated building sensor data,
- Storage of readings in a local database,
- A simple forecasting mechanism using a moving average model.

The implementation uses **FastAPI**, **SQLite**, and **SQLAlchemy** for backend logic and data persistence.

---

## 🧱 Architecture Overview

### **Core Components**
| Module | Description |
|---------|-------------|
| `app/main.py` | FastAPI application, API endpoints (`/ingest`, `/forecast`) |
| `app/database.py` | Database connection setup (SQLite) |
| `app/models.py` | ORM models for sensor readings |
| `data/processed/subset_data.csv` | Small subset of Building Data Genome II used for simulation |
| `decoder.db` | Local SQLite database (auto-created) |

### **Architecture Diagram (Text Description)**

