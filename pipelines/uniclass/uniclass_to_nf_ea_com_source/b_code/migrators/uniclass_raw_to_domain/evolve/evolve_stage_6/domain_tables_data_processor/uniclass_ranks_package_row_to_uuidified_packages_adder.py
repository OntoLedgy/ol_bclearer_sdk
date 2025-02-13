import pandas
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    EA_OBJECT_NAME_COLUMN_NAME,
    EA_OBJECT_TYPE_COLUMN_NAME,
    PACKAGE_NAME,
    PARENT_EA_ELEMENT_COLUMN_NAME,
    UNICLASS_PACKAGE_NAME,
    UNICLASS_RANKS_NAME,
    UUID_COLUMN_NAME,
    UUIDIFIED_PACKAGES_TABLE_NAME,
)


def add_uniclass_ranks_package_row_to_uuidified_packages(
    dictionary_of_dataframes: dict,
) -> dict:
    uuidified_packages_table = dictionary_of_dataframes[
        UUIDIFIED_PACKAGES_TABLE_NAME
    ]

    uniclass_ranks_package_uuid = (
        create_new_uuid()
    )

    uniclass_ranks_package_parent_ea_element_nf_uuid = (
        uuidified_packages_table.loc[
            uuidified_packages_table[
                EA_OBJECT_NAME_COLUMN_NAME
            ]
            == UNICLASS_PACKAGE_NAME,
            UUID_COLUMN_NAME,
        ]
        .to_string(index=False)
        .strip()
    )

    uniclass_rank_item_dataframe = pandas.DataFrame(
        [
            {
                UUID_COLUMN_NAME: uniclass_ranks_package_uuid,
                PARENT_EA_ELEMENT_COLUMN_NAME: uniclass_ranks_package_parent_ea_element_nf_uuid,
                EA_OBJECT_TYPE_COLUMN_NAME: PACKAGE_NAME,
                EA_OBJECT_NAME_COLUMN_NAME: UNICLASS_RANKS_NAME,
            },
        ],
    )

    uuidified_packages = pandas.concat(
        [
            uuidified_packages_table,
            uniclass_rank_item_dataframe,
        ],
        ignore_index=True,
    )

    dictionary_of_dataframes[
        UUIDIFIED_PACKAGES_TABLE_NAME
    ] = uuidified_packages

    return dictionary_of_dataframes
