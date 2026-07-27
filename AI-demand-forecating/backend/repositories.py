from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError


def serialize_document(
    document: Dict[str, Any]
) -> Dict[str, Any]:
    serialized = document.copy()

    if "_id" in serialized:
        serialized["id"] = str(
            serialized.pop("_id")
        )

    return serialized


class ProductRepository:
    def __init__(self, database: Database) -> None:
        self.collection: Collection = database["products"]

        self.collection.create_index(
            [
                ("store", 1),
                ("department", 1),
                ("product_name", 1)
            ],
            unique=True
        )

    def create(
        self,
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)

        document = {
            **product_data,
            "created_at": now,
            "updated_at": now
        }

        try:
            result = self.collection.insert_one(document)

        except DuplicateKeyError as error:
            raise ValueError(
                "This product already exists for the "
                "selected store and department."
            ) from error

        created_product = self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if created_product is None:
            raise RuntimeError(
                "Product was created but could not be retrieved."
            )

        return serialize_document(created_product)

    def get_all(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        cursor = (
            self.collection
            .find()
            .sort("created_at", -1)
            .limit(limit)
        )

        return [
            serialize_document(document)
            for document in cursor
        ]

    def get_by_id(
        self,
        product_id: str
    ) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(product_id):
            return None

        document = self.collection.find_one(
            {"_id": ObjectId(product_id)}
        )

        if document is None:
            return None

        return serialize_document(document)

    def update(
        self,
        product_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        if not ObjectId.is_valid(product_id):
            return None

        update_data["updated_at"] = datetime.now(
            timezone.utc
        )

        result = self.collection.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )

        if result is None:
            return None

        return serialize_document(result)

    def delete(self, product_id: str) -> bool:
        if not ObjectId.is_valid(product_id):
            return False

        result = self.collection.delete_one(
            {"_id": ObjectId(product_id)}
        )

        return result.deleted_count == 1


class PredictionRepository:
    def __init__(self, database: Database) -> None:
        self.collection: Collection = database[
            "predictions"
        ]

        self.collection.create_index(
            "created_at"
        )

        self.collection.create_index(
            "product_id"
        )

    def create(
        self,
        prediction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        document = {
            **prediction_data,
            "created_at": datetime.now(timezone.utc)
        }

        result = self.collection.insert_one(document)

        saved_prediction = self.collection.find_one(
            {"_id": result.inserted_id}
        )

        if saved_prediction is None:
            raise RuntimeError(
                "Prediction could not be retrieved."
            )

        return serialize_document(saved_prediction)

    def get_recent(
        self,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        cursor = (
            self.collection
            .find()
            .sort("created_at", -1)
            .limit(limit)
        )

        return [
            serialize_document(document)
            for document in cursor
        ]
    

    def get_dashboard_summary(
        self
    ) -> Dict[str, Any]:
        total_predictions = self.collection.count_documents(
            {}
        )

        reorder_count = self.collection.count_documents(
            {"reorder_required": True}
        )

        high_risk_count = self.collection.count_documents(
            {"stock_status": "High Risk"}
        )

        overstock_count = self.collection.count_documents(
            {"stock_status": "Overstock Risk"}
        )

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_predicted_demand": {
                        "$sum": "$predicted_demand"
                    },
                    "total_reorder_quantity": {
                        "$sum": "$reorder_quantity"
                    },
                    "average_predicted_demand": {
                        "$avg": "$predicted_demand"
                    }
                }
            }
        ]

        aggregation = list(
            self.collection.aggregate(pipeline)
        )

        totals = (
            aggregation[0]
            if aggregation
            else {}
        )

        return {
            "total_predictions": total_predictions,
            "reorder_count": reorder_count,
            "high_risk_count": high_risk_count,
            "overstock_count": overstock_count,
            "total_predicted_demand": round(
                totals.get(
                    "total_predicted_demand",
                    0
                ),
                2
            ),
            "total_reorder_quantity": round(
                totals.get(
                    "total_reorder_quantity",
                    0
                ),
                2
            ),
            "average_predicted_demand": round(
                totals.get(
                    "average_predicted_demand",
                    0
                ),
                2
            )
        }