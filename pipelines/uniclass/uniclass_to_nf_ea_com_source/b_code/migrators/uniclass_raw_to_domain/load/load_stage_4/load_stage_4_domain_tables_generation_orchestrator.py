from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_dictionary_uuidifier import (
    uuidify_dictionary_of_dataframes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    UNICLASS_LOAD_STAGE_4_DOMAIN_TABLES,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_raw_to_domain.load.load_stage_4.domain_tables_data_processor.load_stage_4_data_domain_tables_exporter import (
    export_load_stage_4_domain_tables,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.services.input_output.all_csv_files_in_resource_namespace_into_dataframe_dictionary_loader import (
    load_all_csv_files_in_resource_namespace_into_dataframe_dictionary,
)


def orchestrate_domain_tables_creation_for_load_stage_4(
    folder_path: str,
    uniclass_source_data_resource_namespace: str,
) -> dict:
    uniclass_2024_dataframe_dictionary = load_all_csv_files_in_resource_namespace_into_dataframe_dictionary(
        resource_namespace=uniclass_source_data_resource_namespace,
    )

    uniclass_2024_uuidified_dataframe_dictionary = uuidify_dictionary_of_dataframes(
        dictionary_of_dataframes=uniclass_2024_dataframe_dictionary,
        uuid_column_name=StandardObjectTableColumnTypes.NF_UUIDS.column_name,
    )

    export_load_stage_4_domain_tables(
        folder_path=folder_path,
        dictionary_of_dataframes=uniclass_2024_uuidified_dataframe_dictionary,
        database_name=UNICLASS_LOAD_STAGE_4_DOMAIN_TABLES,
    )

    return uniclass_2024_uuidified_dataframe_dictionary
