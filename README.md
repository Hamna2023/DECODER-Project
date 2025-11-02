# 🧠 Mini-DECODER Prototype  
**MSc-Level Assignment — DECODER Project (Concordia University)**  

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

![DECODER Architecture Diagram](https://github.com/Hamna2023/DECODER-Project/blob/main/Architecture%20diagram.png)

## ⚙️ Environment Setup

```bash
# Clone the repository
git clone https://github.com/Hamna2023/DECODER-Project.git
cd DECODER-Project

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # On macOS/Linux
# .\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# run backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# run frontend
streamlit run ui/decoder_ui.py


