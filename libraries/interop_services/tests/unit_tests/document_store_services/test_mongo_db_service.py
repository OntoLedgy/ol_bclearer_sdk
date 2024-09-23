import pytest
from bclearer_interop_services.document_store_services.mongo_db_service.mongo_db_wrapper import MongoDBWrapper

class TestMongoDBService():
    @pytest.fixture(autouse=True)
    def setup_method(self):

        self.mongo_wrapper = MongoDBWrapper(
            uri="mongodb://192.168.0.3:27017",
            database_name="default")

        # Insert sample documents
        self.sample_docs = [
            {"id":1234, "name": "Alice", "age": 28, "city": "New York"},
            {"id":1235, "name": "Bob", "age": 24, "city": "San Francisco"},
            {"id":1235, "name": "Bob", "age": 25, "city": "San Francisco"},
        ]
    def test_insert_documents(self):
        self.mongo_wrapper.insert_documents(
            "sample_collection_persons_2",
            self.sample_docs)

    def test_upsert_documents(self):
        self.mongo_wrapper.upsert_documents(
            collection_name="sample_collection_persons_3",
            documents=self.sample_docs,
            primary_key_field="id"
        )
    def test_mongo_db_insert_from_json(self):
        # Insert the sample data into the collection
        self.mongo_wrapper.insert_documents_from_json(
            "configuration",
            "./data/input/mongodb/configuration.json")

    def test_mongo_db_read(self):

        docs = self.mongo_wrapper.find_documents("configuration")
        for doc in docs:
            print(doc)

    def test_mongo_db_export(self):
        self.mongo_wrapper.export_documents_to_json(
            "sample_collection", {"age": {"$gt": 25}},
            "./data/output/mongodb/exported_data.json")
