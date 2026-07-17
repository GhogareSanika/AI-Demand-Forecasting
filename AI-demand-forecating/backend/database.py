from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

from backend.config import get_settings


class MongoDatabase:
    def __init__(self) -> None:
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None

    def connect(self) -> None:
        settings = get_settings()

        self.client = MongoClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000
        )

        # Forces MongoDB to verify the connection.
        self.client.admin.command("ping")

        self.database = self.client[
            settings.database_name
        ]

        print(
            f"Connected to MongoDB database: "
            f"{settings.database_name}"
        )

    def close(self) -> None:
        if self.client is not None:
            self.client.close()

        self.client = None
        self.database = None

        print("MongoDB connection closed.")

    def get_database(self) -> Database:
        if self.database is None:
            raise RuntimeError(
                "MongoDB connection has not been initialized."
            )

        return self.database


mongodb = MongoDatabase()