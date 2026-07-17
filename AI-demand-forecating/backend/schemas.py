from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Features expected by the ML model"
    )

    current_stock: float = Field(..., ge=0)

    safety_stock_percentage: float = Field(
        default=0.20,
        ge=0,
        le=1
    )

    product_id: Optional[str] = None

    @field_validator("features")
    @classmethod
    def validate_features_not_empty(
        cls,
        value: Dict[str, float]
    ) -> Dict[str, float]:
        if not value:
            raise ValueError(
                "The features dictionary cannot be empty."
            )
        return value


class PredictionResponse(BaseModel):
    predicted_demand: float
    current_stock: float
    safety_stock: float
    recommended_stock: float
    reorder_quantity: float
    stock_status: str
    reorder_required: bool


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    database_connected: bool = False


class ModelInfoResponse(BaseModel):
    model_name: str
    number_of_features: int
    features: List[str]
    default_safety_stock_percentage: float


class ProductCreate(BaseModel):
    store: int = Field(..., ge=1)
    department: int = Field(..., ge=1)
    product_name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    current_stock: float = Field(..., ge=0)
    unit_price: float = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    current_stock: Optional[float] = Field(
        default=None,
        ge=0
    )
    unit_price: Optional[float] = Field(
        default=None,
        ge=0
    )


class ProductResponse(BaseModel):
    id: str
    store: int
    department: int
    product_name: str
    category: str
    current_stock: float
    unit_price: float
    created_at: datetime
    updated_at: datetime


class PredictionHistoryResponse(BaseModel):
    id: str
    product_id: Optional[str] = None
    predicted_demand: float
    current_stock: float
    safety_stock: float
    recommended_stock: float
    reorder_quantity: float
    stock_status: str
    reorder_required: bool
    created_at: datetime