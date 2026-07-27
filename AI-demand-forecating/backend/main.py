from contextlib import asynccontextmanager
from typing import Any, Dict

from backend.database import mongodb

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.prediction_service import (
    DemandPredictionService
)
from backend.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictionRequest,
    PredictionResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    PredictionHistoryResponse
)
from backend.repositories import (
    PredictionRepository,
    ProductRepository,
)

prediction_service: DemandPredictionService | None = None


def get_product_repository() -> ProductRepository:
    if product_repository is None:
        raise HTTPException(
            status_code=503,
            detail="Product database is unavailable."
        )

    return product_repository


def get_prediction_repository() -> PredictionRepository:
    if prediction_repository is None:
        raise HTTPException(
            status_code=503,
            detail="Prediction database is unavailable."
        )

    return prediction_repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    global prediction_service
    global product_repository
    global prediction_repository

    try:
        prediction_service = DemandPredictionService()

        mongodb.connect()

        database = mongodb.get_database()

        product_repository = ProductRepository(
            database
        )

        prediction_repository = PredictionRepository(
            database
        )

        print("Application services loaded successfully.")

    except Exception as error:
        prediction_service = None
        product_repository = None
        prediction_repository = None

        print(f"Application startup failed: {error}")

    yield

    mongodb.close()

    prediction_service = None
    product_repository = None
    prediction_repository = None


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
@app.get("/health")
def health_check():
    model_loaded = prediction_service is not None

    database_connected = (
        product_repository is not None
        and prediction_repository is not None
    )

    status = (
        "healthy"
        if model_loaded and database_connected
        else "unhealthy"
    )

    return {
        "status": status,
        "model_loaded": model_loaded,
        "database_connected": database_connected
    }

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
    repository = get_prediction_repository()

    try:
        result = service.create_business_prediction(
            supplied_features=request.features,
            current_stock=request.current_stock,
            safety_stock_percentage=(
                request.safety_stock_percentage
            )
        )

        prediction_document = {
            **result,
            "product_id": request.product_id,
            "features": request.features,
            "safety_stock_percentage": (
                request.safety_stock_percentage
            )
        }

        repository.create(
            prediction_document
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
    

#create product endpoint
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    product: ProductCreate
) -> ProductResponse:
    repository = get_product_repository()

    try:
        result = repository.create(
            product.model_dump()
        )

        return ProductResponse(**result)

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        ) from error
    

#get all products
@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(
    limit: int = 100
) -> list[ProductResponse]:
    repository = get_product_repository()

    safe_limit = min(max(limit, 1), 500)

    products = repository.get_all(
        limit=safe_limit
    )

    return [
        ProductResponse(**product)
        for product in products
    ]


#get one product
@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: str
) -> ProductResponse:
    repository = get_product_repository()

    product = repository.get_by_id(
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return ProductResponse(**product)


#update a product
@app.patch(
    "/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: str,
    product_update: ProductUpdate
) -> ProductResponse:
    repository = get_product_repository()

    update_data = product_update.model_dump(
        exclude_none=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No update values were provided."
        )

    product = repository.update(
        product_id,
        update_data
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return ProductResponse(**product)


#delete a product
@app.delete(
    "/products/{product_id}"
)
def delete_product(
    product_id: str
):
    repository = get_product_repository()

    deleted = repository.delete(
        product_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return {
        "message": "Product deleted successfully."
    }


from backend.schemas import PredictionHistoryResponse

@app.get(
    "/predictions",
    response_model=list[PredictionHistoryResponse]
)
def get_prediction_history(limit: int = 50):
    repository = get_prediction_repository()

    predictions = repository.get_recent(limit)

    print(predictions)   # <-- add this

    return [
        PredictionHistoryResponse(**prediction)
        for prediction in predictions
    ]


@app.get("/dashboard/summary")
def dashboard_summary():
    repository = get_prediction_repository()

    return repository.get_dashboard_summary()