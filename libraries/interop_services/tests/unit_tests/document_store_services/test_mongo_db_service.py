import pytest
from bclearer_interop_services.document_store_services.mongo_db_service.mongo_db_wrapper import (
    MongoDBWrapper,
)


class TestMongoDBService:
    @pytest.fixture(autouse=True)
    def setup_method(
        self, mongodb_container
    ):
        self.mongo_wrapper = (
            mongodb_container
        )

        # Insert sample documents
        self.sample_docs = [
            {
                "id": 1234,
                "name": "Alice",
                "age": 28,
                "city": "New York",
            },
            {
                "id": 1235,
                "name": "Bob",
                "age": 24,
                "city": "San Francisco",
            },
            {
                "id": 1235,
                "name": "Bob",
                "age": 25,
                "city": "San Francisco",
            },
        ]

    def test_insert_documents(self):
        self.mongo_wrapper.insert_documents(
            "sample_collection_persons_2",
            self.sample_docs,
        )

    def test_upsert_documents(self):
        self.mongo_wrapper.upsert_documents(
            collection_name="sample_collection_persons_3",
            documents=self.sample_docs,
            primary_key_field="id",
        )

    def test_mongo_db_insert_from_json(
        self,
        mongo_db_configuration_file_path,
    ):
        # Insert the sample data into the collection
        self.mongo_wrapper.insert_documents_from_json(
            "configuration",
            mongo_db_configuration_file_path,
        )

    def test_mongo_db_read(self):
        docs = self.mongo_wrapper.find_documents(
            "configuration",
        )
        for doc in docs:
            print(doc)

    def test_mongo_db_export(
        self,
        mongo_db_output_folder_absolute_path,
    ):
        self.mongo_wrapper.export_documents_to_json(
            "sample_collection",
            {"age": {"$gt": 25}},
            mongo_db_output_folder_absolute_path,
        )

    def test_mongodb_insert(
        self, mongodb_container
    ):

        wrapper = mongodb_container

        # Example test for inserting a document
        document = {
            "_id": 1,
            "name": "Test",
        }
        inserted_id = (
            wrapper.insert_documents(
                "test_collection",
                document,
            )
        )

        assert (
            inserted_id
            == document["_id"]
        )

        # Clean up
        wrapper.access_collection(
            "test_collection"
        ).delete_many({})
