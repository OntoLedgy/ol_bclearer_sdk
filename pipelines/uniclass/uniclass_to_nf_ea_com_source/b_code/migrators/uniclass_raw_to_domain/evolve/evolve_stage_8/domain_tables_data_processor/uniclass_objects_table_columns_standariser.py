from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    CODE_COLUMN_NAME,
    OBJECT_NAME_COLUMN_NAME,
    PARENT_NAMES_COLUMN_NAME,
    PARENT_PACKAGE_NAME_COLUMN_NAME,
    UNICLASS_2024_OBJECT_TABLE_NAME,
)


def standardise_uniclass_objects_table_columns(
    evolve_stage_7_dictionary_of_dataframes: dict,
) -> dict:
    uniclass_objects_table = evolve_stage_7_dictionary_of_dataframes[
        UNICLASS_2024_OBJECT_TABLE_NAME
    ]

    uniclass_objects_table[
        OBJECT_NAME_COLUMN_NAME
    ] = uniclass_objects_table[
        CODE_COLUMN_NAME
    ]

    uniclass_objects_table[
        PARENT_NAMES_COLUMN_NAME
    ] = ""

    uniclass_objects_table[
        PARENT_PACKAGE_NAME_COLUMN_NAME
    ] = "UNICLASS Items"

    evolve_stage_7_dictionary_of_dataframes[
        UNICLASS_2024_OBJECT_TABLE_NAME
    ] = uniclass_objects_table

    return evolve_stage_7_dictionary_of_dataframes
