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
from pipelines.boson.bclearer_boson_1_1_source.b_code.configurations.getters.boson_1_2e_k_configuration_getter_separate_names_and_instances import (
    get_boson_1_2e_k1_configuration_separate_standard_names_and_instances,
    get_boson_1_2e_k2_configuration_bespoke_standard_names_and_instances,
)


@run_and_log_function
def run_visualization_substage_separate_names_and_instances(
    ea_tools_session_manager: EaToolsSessionManagers,
    output_folder_name: str,
    content_universe: NfEaComUniverses,
) -> NfEaComUniverses:
    separated_standard_names_and_instances_universe = __separate_standard_names_and_instances(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        output_folder_name=output_folder_name,
    )

    separated_bespoke_names_and_instances_universe = __separate_bespoke_names_and_instances(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=separated_standard_names_and_instances_universe,
        output_folder_name=output_folder_name,
    )

    return separated_bespoke_names_and_instances_universe


def __separate_standard_names_and_instances(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_universe: NfEaComUniverses,
    output_folder_name: str,
) -> NfEaComUniverses:
    separated_standard_names_and_instances_universe = run_convention_shift_operation_substage(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        convention_shift_operation_configuration=get_boson_1_2e_k1_configuration_separate_standard_names_and_instances(),
    )

    instrument_and_visualize(
        output_folder_name=output_folder_name,
        visualization_substage_output_universe=separated_standard_names_and_instances_universe,
    )

    return separated_standard_names_and_instances_universe


def __separate_bespoke_names_and_instances(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_universe: NfEaComUniverses,
    output_folder_name: str,
) -> NfEaComUniverses:
    separated_bespoke_names_and_instances = run_convention_shift_operation_substage(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        convention_shift_operation_configuration=get_boson_1_2e_k2_configuration_bespoke_standard_names_and_instances(),
    )

    instrument_and_visualize(
        output_folder_name=output_folder_name,
        visualization_substage_output_universe=separated_bespoke_names_and_instances,
    )

    return separated_bespoke_names_and_instances
