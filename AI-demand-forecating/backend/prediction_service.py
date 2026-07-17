from pathlib import Path
from typing import Any, Dict, List

import joblib
import pandas as pd


class DemandPredictionService:
    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parent.parent

        model_path = (
            project_root
            / "models"
            / "demand_prediction_pipeline.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model pipeline was not found at: {model_path}"
            )

        pipeline: Dict[str, Any] = joblib.load(model_path)

        required_keys = {
            "model",
            "features",
            "safety_stock_percentage"
        }

        missing_keys = required_keys - pipeline.keys()

        if missing_keys:
            raise ValueError(
                f"Pipeline is missing keys: {sorted(missing_keys)}"
            )

        self.model = pipeline["model"]
        self.features: List[str] = list(
            pipeline["features"]
        )
        self.default_safety_stock_percentage = float(
            pipeline["safety_stock_percentage"]
        )

    def get_missing_features(
        self,
        supplied_features: Dict[str, float]
    ) -> List[str]:
        return [
            feature
            for feature in self.features
            if feature not in supplied_features
        ]

    def get_unexpected_features(
        self,
        supplied_features: Dict[str, float]
    ) -> List[str]:
        return [
            feature
            for feature in supplied_features
            if feature not in self.features
        ]

    def predict_demand(
        self,
        supplied_features: Dict[str, float]
    ) -> float:
        missing_features = self.get_missing_features(
            supplied_features
        )

        if missing_features:
            raise ValueError(
                "Missing model features: "
                + ", ".join(missing_features)
            )


        #This section ensures that model features are passed in the same order used during training
        #Even when the user sends features in a different order, the API rearranges them correctly
        ordered_input = {
            feature: supplied_features[feature]
            for feature in self.features
        }

        input_df = pd.DataFrame([ordered_input])

        prediction = self.model.predict(input_df)[0]

        # Product demand cannot be negative.
        return max(float(prediction), 0.0)

    @staticmethod
    def classify_stock_status(
        current_stock: float,
        predicted_demand: float,
        recommended_stock: float
    ) -> str:
        if current_stock < predicted_demand:
            return "High Risk"

        if current_stock < recommended_stock:
            return "Medium Risk"

        if current_stock > recommended_stock * 1.5:
            return "Overstock Risk"

        return "Healthy"

    def create_business_prediction(
        self,
        supplied_features: Dict[str, float],
        current_stock: float,
        safety_stock_percentage: float | None = None
    ) -> Dict[str, Any]:
        predicted_demand = self.predict_demand(
            supplied_features
        )

        if safety_stock_percentage is None:
            safety_stock_percentage = (
                self.default_safety_stock_percentage
            )

        safety_stock = (
            predicted_demand
            * safety_stock_percentage
        )

        recommended_stock = (
            predicted_demand
            + safety_stock
        )

        reorder_quantity = max(
            recommended_stock - current_stock,
            0.0
        )

        stock_status = self.classify_stock_status(
            current_stock=current_stock,
            predicted_demand=predicted_demand,
            recommended_stock=recommended_stock
        )

        return {
            "predicted_demand": round(
                predicted_demand,
                2
            ),
            "current_stock": round(
                current_stock,
                2
            ),
            "safety_stock": round(
                safety_stock,
                2
            ),
            "recommended_stock": round(
                recommended_stock,
                2
            ),
            "reorder_quantity": round(
                reorder_quantity,
                2
            ),
            "stock_status": stock_status,
            "reorder_required": reorder_quantity > 0
        }