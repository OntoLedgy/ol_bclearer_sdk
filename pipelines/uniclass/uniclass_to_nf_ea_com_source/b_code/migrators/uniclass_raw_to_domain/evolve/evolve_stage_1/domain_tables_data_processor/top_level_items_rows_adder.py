import pandas as pd
from pandas import DataFrame
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    CODE_COLUMN_NAME,
    TITLE_COLUMN_NAME,
    TOP_ITEMS_TABLE_NAME,
    UUID_COLUMN_NAME,
)


def add_top_level_item_rows_to_dictionary_of_dataframes(
    dictionary_of_dataframes: dict,
) -> dict:
    top_level_dataframe_dictionary = {}

    uniclass_top_item_dataframe = (
        dictionary_of_dataframes[
            TOP_ITEMS_TABLE_NAME
        ]
    )

    for (
        index,
        row,
    ) in (
        uniclass_top_item_dataframe.iterrows()
    ):
        top_level_dataframe_dictionary = __add_top_item_row_to_dataframe(
            dictionary_of_dataframes=dictionary_of_dataframes,
            row=row,
        )

    return (
        top_level_dataframe_dictionary
    )


def __add_top_item_row_to_dataframe(
    dictionary_of_dataframes: dict,
    row,
) -> dict:
    for (
        table_name,
        dataframe,
    ) in (
        dictionary_of_dataframes.items()
    ):
        dataframe_with_top_item = __generate_top_level_row_dataframe(
            row=row,
            dataframe=dataframe,
        )

        dictionary_of_dataframes[
            table_name
        ] = dataframe_with_top_item

    return dictionary_of_dataframes


def __generate_top_level_row_dataframe(
    row,
    dataframe,
) -> DataFrame:
    top_level_row_dictionary = {}

    if (
        row[CODE_COLUMN_NAME]
        in dataframe[CODE_COLUMN_NAME][
            0
        ]
    ):
        top_level_row_dictionary[
            UUID_COLUMN_NAME
        ] = row[UUID_COLUMN_NAME]
        top_level_row_dictionary[
            CODE_COLUMN_NAME
        ] = row[CODE_COLUMN_NAME]
        top_level_row_dictionary[
            TITLE_COLUMN_NAME
        ] = row[TITLE_COLUMN_NAME]

        # Create DataFrame for new row
        new_row_df = pd.DataFrame(
            [top_level_row_dictionary]
        )

        # Concatenate new row to existing DataFrame
        dataframe = pd.concat(
            [dataframe, new_row_df],
            ignore_index=True,
        )

    return dataframe
