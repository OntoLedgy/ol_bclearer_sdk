import os

from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)


def export_nf_ea_com_to_hdf5(
    nf_ea_com_universe: NfEaComUniverses,
    folder_path: str,
):
    bclearer_stage = (
        nf_ea_com_universe.ea_repository.short_name
    )

    current_stage_hdf5_folder_path = (
        os.path.join(
            folder_path,
            bclearer_stage,
            bclearer_stage
            + "_hdf5_export",
        )
    )

    if not os.path.exists(
        current_stage_hdf5_folder_path,
    ):
        os.mkdir(
            current_stage_hdf5_folder_path,
        )

    hdf5_file_path = os.path.join(
        current_stage_hdf5_folder_path,
        bclearer_stage
        + "_hdf5_export.hdf5",
    )

    hdf5_file = Files(
        absolute_path_string=str(
            hdf5_file_path,
        ),
    )

    log_message(
        "STARTING NF EA COM TO HDF5 EXPORT FOR "
        + bclearer_stage,
    )

    nf_ea_com_universe.nf_ea_com_registry.export_registry_to_hdf5(
        hdf5_file=hdf5_file,
    )

    log_message(
        "NF EA COM TO HDF5 EXPORT DONE - "
        + bclearer_stage,
    )
