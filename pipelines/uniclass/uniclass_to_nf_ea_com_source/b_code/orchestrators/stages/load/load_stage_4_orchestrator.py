from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_domain_to_nf_ea_com.load.load_stage_4.nf_ea_com_tables_creation_for_load_stage_4_orchestrator import (
    orchestrate_nf_ea_com_tables_creation_for_load_stage_4,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_nf_ea_com_exporters.export_nf_ea_com_orchestrator import (
    orchestrate_export_nf_ea_com,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_raw_to_domain.load.load_stage_4.load_stage_4_domain_tables_generation_orchestrator import (
    orchestrate_domain_tables_creation_for_load_stage_4,
)


@run_and_log_function
def orchestrate_load_stage_4(
    folder_path: str,
    uniclass_source_data_resource_namespace: str,
) -> dict:
    uniclass_2024_uuidified_dictionary_of_dataframes = orchestrate_domain_tables_creation_for_load_stage_4(
        folder_path=folder_path,
        uniclass_source_data_resource_namespace=uniclass_source_data_resource_namespace,
    )

    load_stage_4_nf_ea_com_tables = orchestrate_nf_ea_com_tables_creation_for_load_stage_4(
        dictionary_of_dataframes=uniclass_2024_uuidified_dictionary_of_dataframes,
    )

    orchestrate_export_nf_ea_com(
        nf_ea_com_dictionary=load_stage_4_nf_ea_com_tables,
        output_folder_path=folder_path,
        bclearer_stage="load_4",
    )

    return uniclass_2024_uuidified_dictionary_of_dataframes
