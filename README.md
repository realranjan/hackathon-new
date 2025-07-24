# Multi-Agent Supply Chain Analysis Platform

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange)](https://streamlit.io/)

---

## 🚚 What is This Project?

A modern, AI-powered platform for real-time supply chain disruption monitoring, risk analysis, and response planning. Built for hackathons, demos, and as a foundation for enterprise supply chain AI solutions.

- **Multi-agent orchestration:** Event monitoring, risk analysis, and LLM-based response planning
- **Real-time simulation:** Simulate or fetch real disruptions (strikes, weather, disasters)
- **Role-based access:** JWT authentication, admin/operator/viewer roles
- **Extensible data connectors:** Local files, Google Sheets, Airtable
- **Production-ready backend:** Modular FastAPI, logging, error handling, and test coverage
- **Frontend dashboard:** Streamlit for real-time monitoring; Next.js for future UI

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Backend
        A[FastAPI app.py] --> B[Agents: event_monitor, risk_analyzer, response_planner]
        A --> C[Routes: shipment, disruption, health]
        A --> D[Auth, DB, Models, Scheduler]
        D --> E[(MySQL DB)]
        B --> E
    end
    subgraph Frontend
        F[Streamlit Dashboard]
        G[Next.js UI (optional)]
    end
    F <--> A
    G <--> A
    A <--> E
```

---

## 🚀 Features
- **Multi-Agent Orchestration:**
  - Event/news/weather/Twitter monitoring agent
  - Inventory/vendor risk analysis agent
  - LLM-based response planner agent (GPT-4 or fallback rules)
- **Real-Time Disruption Simulation:**
  - Simulate or fetch real disruptions
  - Periodic background checks and alerting
- **Role-Based Access & Auth:**
  - JWT authentication, admin/operator/viewer roles
  - Fine-grained permissions for all endpoints
- **Extensible Data Connectors:**
  - Inventory and vendor data from local files, Google Sheets, or Airtable
- **Production-Ready Backend:**
  - Modular FastAPI codebase, logging, error handling, and test coverage
- **Frontend Dashboard:**
  - Streamlit dashboard for real-time monitoring and simulation
  - Next.js frontend scaffolded for future enterprise UI

---

## 🏁 Quickstart

1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd hackathon_project_multiagent_suppply vhain analysis
   ```
2. **Backend setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Set up your .env file (see backend/README.md for troubleshooting)
   uvicorn app:app --reload
   ```
3. **Frontend (Streamlit):**
   ```bash
   cd ../frontend
   streamlit run app.py
   ```
4. **(Optional) Next.js frontend:**
   ```bash
   cd ../frontend-next
   npm install
   npm run dev
   ```

---

## 🗂️ Project Structure

```
project-root/
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   ├── auth.py
│   ├── scheduler.py
│   ├── routes/
│   ├── agents/
│   ├── utils/
│   ├── tests/
│   └── README.md
├── frontend/
│   └── app.py
├── frontend-next/
│   └── ...
├── data/
│   ├── inventory.json
│   └── vendors.csv
├── requirements.txt
├── README.md
└── ...
```

---

## 🧪 Demo Flow

1. Start backend and frontend
2. Register/login as admin/operator/viewer
3. Simulate a disruption (via API or dashboard)
4. See agent pipeline: event → risk → response
5. View real-time alerts, agent logs, and analytics in dashboard

---

## 🧠 Agents, API, and ML
- **Agents:** Modular Python classes for event monitoring, risk analysis, and response planning
- **API:** FastAPI endpoints for registration, login, simulation, shipment updates, and more
- **ML/AI:**
  - Rule-based risk scoring (can be swapped for ML models)
  - LLM-based response planner (GPT-4 or fallback)
  - Easily extensible for demand forecasting, advanced ML, or external APIs

---

## 🛠️ Troubleshooting
See [`backend/README.md`](backend/README.md) for:
- MySQL connection errors
- .env setup and environment variable loading
- Debugging agent/data issues

---

## 🤝 Contributing
- Fork the repo and create a feature branch
- Add your feature or fix
- Write tests if possible
- Open a pull request!

---

## 📄 License
MIT 