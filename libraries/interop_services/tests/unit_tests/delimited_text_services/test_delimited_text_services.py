from bclearer_interop_services.delimited_text.delimited_text_read import (
    get_table_from_csv_with_header_with_encoding_detection,
)


class TestExcelInteropServices:
    def test_read_csv_with_encoding_detection(
        self,
        csv_file_name_and_path,
    ):
        # Call the function that reads the CSV with encoding detection
        table = get_table_from_csv_with_header_with_encoding_detection(
            csv_file_name_and_path,
        )

        # Assert that the table is not empty
        assert (
            not table.empty
        ), "The table is empty."

        # Assert the shape of the DataFrame (14 rows and 3 columns)
        assert table.shape == (
            14,
            3,
        ), f"DataFrame does not have the expected shape. Expected (14, 3), got {table.shape}."

        # Optionally: check the column names
        expected_columns = [
            "Code",
            "Name",
            "Description",
        ]  # Replace '...' with the actual column names
        assert (
            list(table.columns)
            == expected_columns
        ), f"Unexpected column names: {list(table.columns)}"

        # Optionally: check the content of the first row
        assert (
            table.iloc[0]["Code"] == "E"
        ), "The first row 'Code' column value is not 'E'."

        # Optionally: check the content of the last row
        assert (
            table.iloc[13]["Code"]
            == "M"
        ), "The last row 'Code' column value is not 'M'."

        # Print the table to verify the content
        print(table)

    def test_read_csv_with_header_with_encoding_detection(
        self,
        csv_file_name_and_path_no_header,
    ):
        custom_header = [
            "Code",
            "Name",
            "Description",
        ]

        table = get_table_from_csv_with_header_with_encoding_detection(
            csv_file_name_and_path_no_header,
            custom_header=custom_header,
        )

        # Assert that the table is not empty
        assert (
            not table.empty
        ), "The table is empty."

        # Assert the shape of the DataFrame (14 rows and 3 columns)
        assert table.shape == (
            14,
            3,
        ), f"DataFrame does not have the expected shape. Expected (14, 3), got {table.shape}."

        # Optionally: check the column names
        expected_columns = [
            "Code",
            "Name",
            "Description",
        ]  # Replace '...' with the actual column names
        assert (
            list(table.columns)
            == expected_columns
        ), f"Unexpected column names: {list(table.columns)}"

        # Optionally: check the content of the first row
        assert (
            table.iloc[0]["Code"] == "E"
        ), "The first row 'Code' column value is not 'E'."

        # Optionally: check the content of the last row
        assert (
            table.iloc[13]["Code"]
            == "M"
        ), "The last row 'Code' column value is not 'M'."

        print(table)
