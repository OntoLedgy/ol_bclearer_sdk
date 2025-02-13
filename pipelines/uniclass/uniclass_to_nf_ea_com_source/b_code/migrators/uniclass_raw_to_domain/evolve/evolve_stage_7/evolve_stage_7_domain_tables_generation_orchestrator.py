from bclearer_interop_services.file_system_service.new_folder_creator import (
    create_new_folder,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.common_constants.uniclass_bclearer_constants import (
    EVOLVE_STAGE_7_NAME,
    UNICLASS_EVOLVE_STAGE_7_DOMAIN_TABLES,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_raw_to_domain.evolve.evolve_stage_7.domain_tables_data_processor.evolve_stage_7_domain_tables_getter import (
    get_evolve_stage_7_domain_tables,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.services.input_output.dataframes_dictionary_to_csv_and_access_exporter import (
    export_dataframes_dictionary_to_csv_and_access,
)


def orchestrate_domain_tables_creation_for_evolve_7(
    folder_path: str,
    dictionary_of_dataframes: dict,
) -> dict:
    evolve_stage_7_domain_tables = get_evolve_stage_7_domain_tables(
        dictionary_of_dataframes=dictionary_of_dataframes,
    )

    evolve_stage_7_folder_path = create_new_folder(
        parent_folder_path=folder_path,
        new_folder_name=EVOLVE_STAGE_7_NAME,
    )

    evolve_stage_7_domain_tables_folder_path = create_new_folder(
        parent_folder_path=evolve_stage_7_folder_path,
        new_folder_name=EVOLVE_STAGE_7_NAME
        + "_domain_tables",
    )

    export_dataframes_dictionary_to_csv_and_access(
        dictionary_of_dataframes=evolve_stage_7_domain_tables,
        folder_path=evolve_stage_7_domain_tables_folder_path,
        database_name=UNICLASS_EVOLVE_STAGE_7_DOMAIN_TABLES,
    )

    return evolve_stage_7_domain_tables
