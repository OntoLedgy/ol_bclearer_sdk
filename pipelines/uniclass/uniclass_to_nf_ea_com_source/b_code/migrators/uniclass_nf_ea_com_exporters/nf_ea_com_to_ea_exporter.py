import os

from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.domain_to_nf_ea_com_migration.orchestrators.nf_ea_com_universe_to_eapx_migration_orchestator import (
    orchestrate_nf_ea_com_universe_to_eapx_migration,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def export_nf_ea_com_to_ea(
    ea_tools_session_manager: EaToolsSessionManagers,
    nf_ea_com_universe: NfEaComUniverses,
    folder_path: str,
):
    bclearer_stage = (
        nf_ea_com_universe.ea_repository.short_name
    )

    current_stage_ea_export_folder_path = os.path.join(
        folder_path,
        bclearer_stage,
        bclearer_stage + "_ea_export",
    )

    if not os.path.exists(
        current_stage_ea_export_folder_path,
    ):
        os.mkdir(
            current_stage_ea_export_folder_path,
        )

    log_message(
        "STARTING EA EXPORT (XML) FOR "
        + bclearer_stage,
    )

    orchestrate_nf_ea_com_universe_to_eapx_migration(
        ea_tools_session_manager=ea_tools_session_manager,
        nf_ea_com_universe=nf_ea_com_universe,
        short_name=bclearer_stage,
        output_folder=Folders(
            absolute_path_string=folder_path,
        ),
    )

    log_message(
        "EA EXPORT DONE (XML) - "
        + bclearer_stage,
    )
