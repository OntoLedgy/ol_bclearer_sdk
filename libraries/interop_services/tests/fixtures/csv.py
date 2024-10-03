import os
import random

import pandas as pd
import pytest
from faker import Faker


@pytest.fixture(scope="module")
def csv_file(
    data_input_folder_absolute_path,
):
    input_csv_file_relative_path = r"delimited_text/cfi-20210507-current_no_header.csv"

    input_csv_file_absolute_path = os.path.join(
        data_input_folder_absolute_path,
        input_csv_file_relative_path,
    )

    return input_csv_file_absolute_path


@pytest.fixture(scope="module")
def sample_transactions_csv_file(
    data_input_folder_absolute_path,
):

    input_csv_file_relative_path = r"delimited_text/generated_files/sample_transactions.csv"

    # Initialize Faker for generating random data
    fake = Faker()

    # Generate random data for the transactions table
    data = {
        "transaction_date": [
            fake.date_this_year()
            for _ in range(10)
        ],  # Random date within this year
        "amount": [
            round(
                random.uniform(
                    10.0, 1000.0
                ),
                2,
            )
            for _ in range(10)
        ],  # Random amount
        "description": [
            fake.sentence()
            for _ in range(10)
        ],  # Random description
    }

    # Create a DataFrame
    df_transactions = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    csv_file_path = os.path.join(
        data_input_folder_absolute_path,
        input_csv_file_relative_path,
    )

    os.makedirs(
        os.path.dirname(csv_file_path),
        exist_ok=True,
    )

    df_transactions.to_csv(
        csv_file_path, index=False
    )

    return csv_file_path
