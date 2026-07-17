## Current Progress

- [x] Project setup
- [x] Exploratory Data Analysis
- [x] Data preprocessing
- [x] Time-series feature engineering
- [x] Model training and evaluation
- [x] Demand prediction pipeline
- [x] Inventory recommendation logic
- [x] Explainable AI
- [x] FastAPI backend
- [ ] MongoDB integration
- [ ] React frontend
- [ ] Frontend-backend integration
- [ ] Deployment

## Backend API

The FastAPI backend loads the trained XGBoost demand-forecasting model and provides inventory recommendations.

### Available Endpoints

- `GET /` – API information
- `GET /health` – Model health check
- `GET /model-info` – Model feature information
- `GET /sample-request` – Sample request structure
- `POST /predict` – Demand and inventory prediction

### Run Locally

```bash
uvicorn backend.main:app --reload