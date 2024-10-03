import sys

from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from ea_interop_service_source.b_code.return_results.i_dual_repository_creation_result_types import (
    IDualRepositoryCreationResultTypes,
)
from ea_interop_service_source.b_code.return_results.i_dual_repository_creation_results import (
    IDualRepositoryCreationResults,
)


def report_i_dual_repository_creation_result(
    i_dual_repository_creation_result: IDualRepositoryCreationResults,
    ea_project_filename: str,
):
    i_dual_repository_creation_result_type = (
        i_dual_repository_creation_result.i_dual_repository_creation_result_type
    )

    if (
        i_dual_repository_creation_result_type
        == IDualRepositoryCreationResultTypes.SUCCEEDED
    ):
        log_message(
            "Opened EA project: "
            + ea_project_filename
        )

        return

    if (
        i_dual_repository_creation_result_type
        == IDualRepositoryCreationResultTypes.FAILED_TO_OPEN_EA
    ):
        log_message("Failed to open EA")

    if (
        i_dual_repository_creation_result_type
        == IDualRepositoryCreationResultTypes.FAILED_TO_OPEN_EA_PROJECT
    ):
        log_message(
            "Failed to open EA project: "
            + ea_project_filename
        )

    else:
        log_message(
            "Unhandled type: "
            + str(
                i_dual_repository_creation_result_type
            )
        )

    sys.exit(-1)
