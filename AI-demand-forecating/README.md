## Current Progress


- [x] Project setup
- [x] Exploratory Data Analysis
- [x] Data preprocessing
- [x] Feature engineering
- [x] Model training and evaluation
- [x] Prediction and inventory logic
- [x] FastAPI backend
- [x] MongoDB Atlas integration
- [x] Product and prediction-history APIs
- [ ] React frontend
- [ ] Frontend-backend integration
- [ ] Dashboard visualizations
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

## MongoDB Integration

MongoDB Atlas is used to persist product inventory and prediction history.

### Collections

- `products` – Stores product and current inventory information
- `predictions` – Stores model predictions and inventory recommendations

### Database Endpoints

- `POST /products` – Add a product
- `GET /products` – List products
- `GET /products/{id}` – Get one product
- `PATCH /products/{id}` – Update a product
- `DELETE /products/{id}` – Delete a product
- `GET /predictions` – View prediction history
- `GET /dashboard/summary` – View dashboard KPIs

### Environment Variables

Create a `.env` file:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=demand_forecasting