from bclearer_core.substages.operations.b_evolve.convention_shift_operations.runners.convention_shift_operations_substage_runner import (
    run_convention_shift_operation_substage,
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
from pipelines.boson.bclearer_boson_1_1_source.b_code.configurations.getters.boson_1_2e_j_configuration_getter_generalise_names import (
    get_boson_1_2e_j1_configuration_generalise_names,
)


@run_and_log_function
def run_visualization_substage_generalise_names(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
    content_universe: NfEaComUniverses,
) -> NfEaComUniverses:
    generalised_names_universe = run_convention_shift_operation_substage(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        convention_shift_operation_configuration=get_boson_1_2e_j1_configuration_generalise_names(),
    )

    instrument_and_visualize(
        output_folder_name=output_folder_name,
        visualization_substage_output_universe=generalised_names_universe,
    )

    return generalised_names_universe
