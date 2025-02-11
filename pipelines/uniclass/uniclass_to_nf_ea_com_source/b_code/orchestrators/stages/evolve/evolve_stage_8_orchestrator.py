from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_domain_to_nf_ea_com.evolve.evolve_stage_8.nf_ea_com_tables_creation_for_evolve_stage_8_orchestrator import (
    orchestrate_nf_ea_com_tables_creation_for_evolve_stage_8,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_nf_ea_com_exporters.export_nf_ea_com_orchestrator import (
    orchestrate_export_nf_ea_com,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.migrators.uniclass_raw_to_domain.evolve.evolve_stage_8.evolve_stage_8_domain_tables_generation_orchestrator import (
    orchestrate_domain_tables_creation_for_evolve_8,
)


@run_and_log_function
def orchestrate_evolve_stage_8(
    evolve_stage_7_dictionary_of_dataframes: dict,
    folder_path: str,
) -> dict:
    uniclass_2024_domain_tables = orchestrate_domain_tables_creation_for_evolve_8(
        folder_path=folder_path,
        evolve_stage_7_dictionary_of_dataframes=evolve_stage_7_dictionary_of_dataframes,
    )

    evolve_stage_8_nf_ea_com_tables = orchestrate_nf_ea_com_tables_creation_for_evolve_stage_8(
        dictionary_of_dataframes=uniclass_2024_domain_tables,
    )

    orchestrate_export_nf_ea_com(
        nf_ea_com_dictionary=evolve_stage_8_nf_ea_com_tables,
        output_folder_path=folder_path,
        bclearer_stage="evolve_8",
    )

    return uniclass_2024_domain_tables
