from bclearer_core.substages.operations.b_evolve.adjustment_operations.runners.adjustment_operations_substage_runner import (
    run_adjustment_operations_substage,
)
from bclearer_core.substages.visualizations.instrumentation_and_visualization_runner import (
    instrument_and_visualize,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)
from pipelines.boson.bclearer_boson_1_1_source.b_code.configurations.getters.boson_1_2e_b_configuration_getter_clean_inspire import (
    get_boson_1_2e_b_configuration_clean_inspire,
)


@run_and_log_function
def run_visualization_substage_clean_inspire_os_model(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
    content_universe: NfEaComUniverses,
) -> NfEaComUniverses:
    os_inspire_filtered_universe = run_adjustment_operations_substage(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        adjustment_operations_substage_configuration=get_boson_1_2e_b_configuration_clean_inspire(),
    )

    instrument_and_visualize(
        output_folder_name=output_folder_name,
        visualization_substage_output_universe=os_inspire_filtered_universe,
    )

    return os_inspire_filtered_universe
