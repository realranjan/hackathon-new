# SupplyWhiz – AI-Powered Supply Chain Disruption Assistant

SupplyWhiz is a multi-agent AI system designed to help logistics and operations teams handle real-time disruptions in the supply chain. It leverages GPT-4, LangChain/LangGraph agents, and FastAPI, with an interactive Streamlit dashboard for visualization. An experimental Next.js frontend is also included.

---

## 🚀 Features

- **Agent 1: News & Event Monitor**
  - Monitors news, weather, and social feeds for supply chain disruptions (strike, port closure, disaster, protest, etc.)
  - Falls back to simulation if no real events are found
- **Agent 2: Inventory Risk Analyzer**
  - Matches disruptions to inventory and vendor data, flags at-risk shipments
  - Calculates risk scores based on event severity and product criticality
- **Agent 3: Response Planner**
  - Uses GPT-4 (or fallback rules) to suggest alternate routes/vendors, mitigation steps, and generates alert messages
- **Backend Orchestration (FastAPI):**
  - Orchestrates the agent pipeline and exposes API endpoints for simulating events and fetching alerts
  - Periodically checks for disruptions and persists alerts
- **Frontend (Streamlit Dashboard):**
  - Real-time dashboard to simulate disruptions, view alerts, agent logs, analytics, and a disruption map
- **Experimental Next.js Frontend:**
  - Scaffolded for future extensibility; not integrated in the main flow
- **Bonus:**
  - Agent reasoning log, risk scoring, and demo/test case

---

## 🗂️ Project Structure

```
SupplyWhiz/
├── agents/
│   ├── event_monitor.py         # Event/news/weather/Twitter monitoring
│   ├── risk_analyzer.py         # Inventory/vendor risk analysis
│   └── response_planner.py      # LLM-based response planning
├── data/
│   ├── vendors.csv              # Vendor data
│   └── inventory.json           # Inventory/shipment data
├── utils/
│   └── data_loader.py           # Data and API key loading utilities
├── frontend/
│   └── app.py                   # Streamlit dashboard
├── frontend-next/               # Experimental Next.js frontend
├── main.py                      # FastAPI backend entrypoint
├── requirements.txt
├── alerts.json                  # Persisted alerts
└── README.md
```

---

## ⚙️ How It Works

1. **Event Monitor** scrapes or simulates disruptions (e.g., port strikes, weather events, disasters)
2. **Risk Analyzer** checks if inventory/shipments are affected and calculates risk scores
3. **Response Planner** uses GPT-4 (or fallback rules) to suggest mitigations and generate alerts
4. **Backend** orchestrates the agent pipeline and exposes API endpoints
5. **Frontend (Streamlit)** displays real-time alerts, agent logs, analytics, and a disruption map

---

## 🧪 Simulate a Disruption

- Run the backend (`main.py`)
- (Optional) Start the Streamlit dashboard (`frontend/app.py`)
- Use the dashboard button or API to simulate a disruption (e.g., "strike at Bangalore port")
- Watch the full agent flow and response in real time

---

## 📝 Demo Flow

1. Start backend and frontend
2. Simulate a disruption
3. Show real-time alert, agent reasoning log, and analytics
4. (Optional) Overlay map with affected regions

---

## 📦 Requirements & Setup

- Python 3.9+
- FastAPI
- LangChain or LangGraph
- (Optional) Streamlit
- (Optional) Next.js (for experimental frontend)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment variables
Create a `.env` file with the following (as needed):
```
NEWSAPI_KEY=your_newsapi_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
WEATHERSTACK_KEY=your_weatherstack_key
AVIATIONSTACK_KEY=your_aviationstack_key
MYSHIPTRACKING_KEY=your_myshiptracking_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Run the backend
```bash
python main.py
```

### 4. Run the Streamlit dashboard (optional)
```bash
streamlit run frontend/app.py
```

### 5. (Optional) Next.js frontend
See `frontend-next/README.md` for setup. Not integrated with backend yet.

---

## 📚 Sample Data

- `vendors.csv`: 
  - Columns: `vendor_id`, `location`, `product_type`, `status`
  - Example:
    ```csv
    vendor_id,location,product_type,status
    Vendor_001,Bangalore,Electronics,Active
    Vendor_002,Chennai,Textiles,Active
    Vendor_003,Mumbai,Automotive,Inactive
    ```
- `inventory.json`:
  - List of objects: `product_id`, `vendor_id`, `shipping_origin`, `eta`, `criticality_score`
  - Example:
    ```json
    [
      {"product_id": "P1001", "vendor_id": "Vendor_001", "shipping_origin": "Bangalore", "eta": "2024-06-10", "criticality_score": 90},
      {"product_id": "P1002", "vendor_id": "Vendor_002", "shipping_origin": "Chennai", "eta": "2024-06-12", "criticality_score": 70}
    ]
    ```

---

## 🤖 Agent Prompts & Logic

- **Event Monitor:** Fetches disruptions from news, weather, Twitter, or simulates if none found.
- **Risk Analyzer:** Flags at-risk shipments by matching event location to vendor/inventory data and calculates risk scores.
- **Response Planner:** Uses GPT-4 (if available) to suggest alternate routes/vendors, mitigation steps, and generates alert messages. Falls back to rule-based logic if LLM is unavailable.

---

## 🖥️ Streamlit Dashboard Features

- Simulate disruptions with a button
- View real-time alerts, agent logs, and action plans
- Map overlay for disruption locations
- Analytics: total alerts, average risk score, event type distribution

---

## 🧩 Extensibility & Future Scalability

- **Plug-and-play agents:** Add new agents for other data sources or risk types
- **Data connectors:** Supports Google Sheets, Airtable, and can be extended to other sources
- **Frontend:** Next.js frontend can be developed for enterprise-grade UI
- **Cloud deployment:** Easily containerized for cloud or on-prem deployment
- **LLM upgrades:** Swap in more advanced LLMs or custom models as needed

---

## License

MIT 

---

## 🌐 External Data Connectors & APIs

SupplyWhiz supports flexible data sourcing for inventory and vendor data, as well as real-time event monitoring using multiple APIs. You can use local files, Google Sheets, Airtable, and more.

### 1. Data Connectors

#### a. **Google Sheets for Inventory Data**
- **Purpose:** Load inventory data from a Google Sheet instead of `data/inventory.json`.
- **How to Use:**
  1. Create a Google Service Account and download the credentials JSON file.
  2. Set the path to your credentials file in the `.env` as `GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json` (or your filename).
  3. Call the loader with `use_gsheet=True`, e.g.:
     ```python
     from utils.data_loader import load_inventory
     inventory = load_inventory(use_gsheet=True, gsheet_id="your_sheet_id", worksheet_name="Sheet1")
     ```
  4. Install dependencies:
     ```bash
     pip install gspread google-auth
     ```

#### b. **Airtable for Vendor Data**
- **Purpose:** Load vendor data from Airtable instead of `data/vendors.csv`.
- **How to Use:**
  1. Get your Airtable API key, Base ID, and Table Name.
  2. Call the loader with `use_airtable=True`, e.g.:
     ```python
     from utils.data_loader import load_vendors
     vendors = load_vendors(use_airtable=True, airtable_api_key="your_key", airtable_base_id="your_base_id", airtable_table_name="Vendors")
     ```
  3. Install dependency:
     ```bash
     pip install pyairtable
     ```

#### c. **Fallback to Local Files**
- If you do not enable these connectors, the system will use the local files in `data/` by default.

### 2. Event & AI APIs

- **NewsAPI:** For news-based disruption detection. Requires `NEWSAPI_KEY` in `.env`.
- **WeatherStack:** For weather-based disruption detection. Requires `WEATHERSTACK_KEY` in `.env`.
- **Twitter API:** For social media-based disruption detection. Requires `TWITTER_API_KEY` and `TWITTER_API_SECRET` in `.env`.
- **OpenAI API:** For GPT-4-based response planning. Requires `OPENAI_API_KEY` in `.env`.

### 3. Example `.env` File
```
NEWSAPI_KEY=your_newsapi_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
WEATHERSTACK_KEY=your_weatherstack_key
AVIATIONSTACK_KEY=your_aviationstack_key
MYSHIPTRACKING_KEY=your_myshiptracking_key
GROQ_API_KEY=your_groq_api_key
```

### 4. Extra Dependencies
If you use Google Sheets or Airtable connectors, install the required packages:
```bash
pip install gspread google-auth pyairtable
```

--- 

---

## 🔄 Data Source Flexibility: Local Files, Google Sheets, Airtable

SupplyWhiz supports loading inventory and vendor data from local files, Google Sheets, or Airtable. By default, it uses local files, but you can switch to cloud sources with a few code changes.

### **Local Files (Default)**
- Inventory: `data/inventory.json`
- Vendors: `data/vendors.csv`

### **Google Sheets (for Inventory)**
- To enable, use the `load_inventory` function from `utils/data_loader.py` with `use_gsheet=True` and provide your Google Sheet ID and worksheet name.
- Requires a Google Service Account JSON file and the `gspread`/`google-auth` packages.
- Example code (see comments in `agents/risk_analyzer.py`):
  ```python
  from utils.data_loader import load_inventory
  import os
  inventory = load_inventory(
      use_gsheet=True,
      gsheet_id=os.getenv("GSHEET_ID"),
      worksheet_name=os.getenv("GSHEET_WORKSHEET", "Sheet1")
  )
  ```
- Add to your `.env`:
  ```
  GSHEET_ID=your_google_sheet_id
  GSHEET_WORKSHEET=Sheet1
  GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
  ```

### **Airtable (for Vendors)**
- To enable, use the `load_vendors` function from `utils/data_loader.py` with `use_airtable=True` and provide your Airtable API key, base ID, and table name.
- Requires the `pyairtable` package.
- Example code (see comments in `agents/risk_analyzer.py`):
  ```python
  from utils.data_loader import load_vendors
  import os
  vendors = load_vendors(
      use_airtable=True,
      airtable_api_key=os.getenv("AIRTABLE_API_KEY"),
      airtable_base_id=os.getenv("AIRTABLE_BASE_ID"),
      airtable_table_name=os.getenv("AIRTABLE_TABLE_NAME")
  )
  ```
- Add to your `.env`:
  ```
  AIRTABLE_API_KEY=your_airtable_api_key
  AIRTABLE_BASE_ID=your_airtable_base_id
  AIRTABLE_TABLE_NAME=your_airtable_table_name
  ```

---

## 🟢 Real API Usage vs Simulation

- The backend tries to use real APIs (AviationStack, MyShipTracking, NewsAPI, WeatherStack, Twitter) for disruption events.
- If no real events are found or API keys are missing/invalid, it falls back to simulation.
- **Every event now includes a `data_source` field:**
  - `"data_source": "real"` means the event came from a real API.
  - `"data_source": "simulated"` means the event is a fallback/mock.
- Check this field in `alerts.json` or the dashboard to know the source of your data.

---

## 🚚 Real-Time GPS Tracking & Simulation

### **A. GPS Simulator (Demo/Testing)**
- Use `utils/gps_simulator.py` to simulate GPS updates for any or all shipments.
- The simulator moves each shipment along its route, updating the backend and dashboard in real time.
- Example usage:
  ```bash
  python utils/gps_simulator.py --product_id P1001
  python utils/gps_simulator.py --all
  ```
- The dashboard and risk analyzer will react as locations change.

### **B. Real Device Integration (Traccar)**
- Register a real GPS device or use the Traccar mobile app to send live location updates to your Traccar server.
- Set the device ID in your shipment and use the `/update_shipment_gps/` endpoint to fetch and update the shipment’s location in real time.
- Example usage:
  ```bash
  curl -X POST http://localhost:8000/update_shipment_gps/ \
    -H "Content-Type: application/json" \
    -d '{"product_id": "P1001", "device_id": "123"}'
  ```
- The backend will reverse-geocode the coordinates and update the shipment’s `current_location`.

- **.env settings for Traccar:**
  ```
  TRACCAR_API=http://localhost:8082/api
  TRACCAR_TOKEN=your_traccar_token
  # Or use TRACCAR_USER and TRACCAR_PASS for basic auth
  ```

---

## ⚙️ Environment Variables

Add these to your `.env` as needed:
```
NEWSAPI_KEY=your_newsapi_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
WEATHERSTACK_KEY=your_weatherstack_key
AVIATIONSTACK_KEY=your_aviationstack_key
MYSHIPTRACKING_KEY=your_myshiptracking_key
GROQ_API_KEY=your_groq_api_key
# For Google Sheets
GSHEET_ID=your_google_sheet_id
GSHEET_WORKSHEET=Sheet1
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
# For Airtable
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
AIRTABLE_TABLE_NAME=your_airtable_table_name
```

---

## 🧪 Testing Real vs Simulated Data

- Use `/fetch_events/air`, `/fetch_events/sea`, `/fetch_events/road` to see if real events are being fetched.
- Simulate an event with `/simulate_event/` if you want to force an alert.
- Check the `data_source` field in the resulting alerts to confirm the source.

--- 

## Backend Structure (after refactor)

- `app.py` — FastAPI app entrypoint, includes routers, middleware, scheduler
- `db.py` — Database connection and password context
- `models.py` — All Pydantic models
- `auth.py` — Auth logic, registration, login, and user dependency
- `routes/` — All API route modules (shipment.py, disruption.py, health.py)
- `scheduler.py` — Scheduler setup and periodic disruption check
- `agents/` — Agent logic (event_monitor.py, risk_analyzer.py, response_planner.py)
- `utils/` — Utility modules (data_loader.py, notifications.py, gps_simulator.py)

**Run the backend with:**

```bash
uvicorn app:app --reload
``` 