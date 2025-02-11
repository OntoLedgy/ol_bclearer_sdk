import os

from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def export_nf_ea_com_to_access(
    ea_tools_session_manager: EaToolsSessionManagers,
    nf_ea_com_universe: NfEaComUniverses,
    folder_path: str,
):
    bclearer_stage = (
        nf_ea_com_universe.ea_repository.short_name
    )

    current_stage_nf_ea_com_export_folder_path = os.path.join(
        folder_path,
        bclearer_stage,
        bclearer_stage + "_nf_ea_com",
    )

    if not os.path.exists(
        current_stage_nf_ea_com_export_folder_path,
    ):
        os.mkdir(
            current_stage_nf_ea_com_export_folder_path,
        )

    log_message(
        "STARTING NF EA COM ACCESS EXPORT FOR "
        + bclearer_stage,
    )

    ea_tools_session_manager.nf_ea_com_endpoint_manager.nf_ea_com_universe_manager.export_all_registries(
        output_folder_name=folder_path,
    )

    log_message(
        "NF EA COM ACCESS EXPORT DONE - "
        + bclearer_stage,
    )
