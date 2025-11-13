# Advertiser Analytics API  
A lightweight FastAPI microservice that exposes revenue, order, customer, and time-series insights through clean REST endpoints. This project extends my original ETL pipeline by transforming the processed dataset into a production-style analytics API — similar to what a Data Engineer or SWE builds for internal dashboards or reporting systems.

---

## 🚀 Features
- Daily, weekly, monthly revenue trends  
- Top advertisers by revenue  
- Summary metrics (revenue, orders, customers)  
- Revenue forecasting (Linear Regression)  
- Auto-cleaning and renaming of raw CSV columns  
- REST API with FastAPI + Uvicorn  
- Fully modular and deploy-ready  

---

## 📁 Project Structure
```
advertiser-analytics-api/
│
├── app/
│   ├── main.py                 # FastAPI application
│   └── __init__.py
│
├── data/
│   └── advertisers_clean.csv   # Cleaned dataset from ETL project
│
├── venv/                       # Virtual environment
├── requirements.txt            # Dependencies
└── README.md
```

---

# 🧠 Architecture Diagram

```mermaid
flowchart TD

    A[Cleaned CSV Dataset\n(advertisers_clean.csv)] --> B[FastAPI App\n(main.py)]
    B --> C[Data Loader\n(pandas)]
    C --> D[Analytics Layer\n(groupby, resample, ML)]
    D --> E[REST Endpoints]

    E --> F[/summary/]
    E --> G[/top_advertisers/]
    E --> H[/trend/]
    E --> I[/predict/]

    style A fill:#f8d568,stroke:#b8860b,stroke-width:2px
    style B fill:#8ec5fc,stroke:#4682b4,stroke-width:2px
    style D fill:#b5e8c2,stroke:#228b22,stroke-width:2px
    style E fill:#f7b2d9,stroke:#b03060,stroke-width:2px
```

---

# 📊 API Endpoints

## 🔹 `GET /health`
Returns schema + row count  
```json
{
  "status": "ok",
  "rows": 68798,
  "columns": ["advertiser","date","spend","orders","customers"]
}
```

---

## 🔹 `GET /summary`
Overall metrics  
```json
{
  "total_revenue": 18923492.19,
  "total_orders": 482399,
  "total_customers": 49113
}
```

---

## 🔹 `GET /top_advertisers?limit=5`
Top advertisers by revenue  
```json
[
  {"advertiser": 1023, "spend": 923421.91},
  {"advertiser": 502, "spend": 812399.33}
]
```

---

## 🔹 `GET /trend?freq=D`
Daily/Weekly/Monthly trend  
```json
[
  {"date": "2017-01-01", "spend": 11234.11},
  {"date": "2017-01-02", "spend": 9981.33}
]
```

---

## 🔹 `GET /predict?days=7`
7–30 day revenue forecasting  
```json
[
  {"date": "2024-02-10", "predicted_revenue": 12231.44},
  {"date": "2024-02-11", "predicted_revenue": 11982.01}
]
```

---

# ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/advertiser-analytics-api.git
cd advertiser-analytics-api
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
```

### 3️⃣ Activate it
```bash
.\venv\Scripts\activate
```

### 4️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Start API server
```bash
uvicorn app.main:app --reload
```

### 6️⃣ Open API documentation  
👉 http://127.0.0.1:8000/docs  

---

# 📈 Tech Stack
- Python 3.11  
- FastAPI  
- Uvicorn  
- Pandas  
- NumPy  
- scikit-learn  
- Mermaid.js  

---

# 🎯 Purpose
This project demonstrates how to:
- Convert an ETL pipeline into a scalable API  
- Serve analytics + ML forecasting through REST endpoints  
- Build real-world data engineering services  
- Structure production-ready Python projects  

---

# 👤 Author
**Errol Brown**  
Data Engineering • Analytics • Python • FastAPI  
