from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.prediction_service import (
    DemandPredictionService
)
from backend.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse
)


prediction_service: DemandPredictionService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global prediction_service

    try:
        prediction_service = DemandPredictionService()
        print("Demand prediction model loaded successfully.")

    except Exception as error:
        prediction_service = None
        print(f"Model loading failed: {error}")

    yield

    prediction_service = None


app = FastAPI(
    title="AI Demand Forecasting API",
    description=(
        "Predict retail demand and generate inventory "
        "recommendations using a trained XGBoost model."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_prediction_service() -> DemandPredictionService:
    if prediction_service is None:
        raise HTTPException(
            status_code=503,
            detail="The prediction model is not available."
        )

    return prediction_service


#Confirms the API is running
@app.get("/")
def home() -> Dict[str, str]:
    return {
        "message": "AI Demand Forecasting API is running",
        "documentation": "/docs"
    }

#Checks whether the model loaded
@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check() -> HealthResponse:
    return HealthResponse(
        status=(
            "healthy"
            if prediction_service is not None
            else "unhealthy"
        ),
        model_loaded=prediction_service is not None
    )

#Returns model name and features
@app.get(
    "/model-info",
    response_model=ModelInfoResponse
)
def model_information() -> ModelInfoResponse:
    service = get_prediction_service()

    return ModelInfoResponse(
        model_name=type(service.model).__name__,
        number_of_features=len(service.features),
        features=service.features,
        default_safety_stock_percentage=(
            service.default_safety_stock_percentage
        )
    )

#Produces a valid request structure
@app.get("/sample-request")
def sample_request() -> Dict[str, Any]:
    service = get_prediction_service()

    sample_features = {
        feature: 0.0
        for feature in service.features
    }

    return {
        "features": sample_features,
        "current_stock": 10000,
        "safety_stock_percentage": (
            service.default_safety_stock_percentage
        )
    }

#Predicts demand and inventory needs
@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(
    request: PredictionRequest
) -> PredictionResponse:
    service = get_prediction_service()

    try:
        result = service.create_business_prediction(
            supplied_features=request.features,
            current_stock=request.current_stock,
            safety_stock_percentage=(
                request.safety_stock_percentage
            )
        )

        return PredictionResponse(**result)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {error}"
        ) from error