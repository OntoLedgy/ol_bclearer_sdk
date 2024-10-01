from bclearer_interop_services.delimited_text.delimited_text_read import \
    get_table_from_csv_with_header_with_encoding_detection

from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.hash_creators.content_hash_column_using_all_columns_adder import add_content_hash_column_using_all_columns

class TestRelationalDatabaseInteropInteropServices:

    def test_database_connection_and_read(
            self,
            db_connection):

        results = db_connection.fetch_results("SELECT * FROM transactions")

        for row in results:
            print(row)

    def test_database_write_dataframe(
            self,
            db_connection,
            csv_file):

        custom_header = [
            "date",
            "description",
            "amount"]

        table = (
                get_table_from_csv_with_header_with_encoding_detection(
                csv_file,
                custom_header=custom_header
            )
        )

        db_connection.store_dataframe(
            table,
            'load_database_transactions')

    def test_database_read_hashify_write(
            self,
            db_connection):

        results = db_connection.fetch_results("SELECT * FROM transactions")

        add_content_hash_column_using_all_columns(
            results)

        db_connection.store_dataframe(
            results,
            'load_database_transactions_hashed')