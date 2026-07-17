from typing import Dict, List

from pydantic import BaseModel, Field, field_validator


class PredictionRequest(BaseModel):
    features: Dict[str, float] = Field(
        ...,
        description="Feature names and values expected by the ML model"
    )

    current_stock: float = Field(
        ...,
        ge=0,
        description="Currently available inventory"
    )

    safety_stock_percentage: float = Field(
        default=0.20,
        ge=0,
        le=1,
        description="Safety-stock percentage between 0 and 1"
    )

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


class ModelInfoResponse(BaseModel):
    model_name: str
    number_of_features: int
    features: List[str]
    default_safety_stock_percentage: float