import pytest
from bclearer_interop_services.file_system_service.all_files_from_file_system_object_paths_getter import (
    get_all_files_from_file_system_object_paths,
)
from bclearer_interop_services.file_system_service.objects.folders import Folders
from bclearer_orchestration_services.b_app_runner_service.logging.logger_initialiser import (
    initialise_logger,
)
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)


class TestFileSystemServices:
    @pytest.fixture(autouse=True)
    def setup(self, log_folder):
        initialise_logger(
            environment_log_level_type=EnvironmentLogLevelTypes.FULL,
            output_folder_prefix="testing_files",
            output_folder_suffix="",
            output_root_folder=Folders(
                log_folder,
            ),
        )
        self.paths = ["file_services"]

    def test_get_all_files_from_file_system_object_paths(
        self,
        storage_interop_services_source_folder,
    ):
        all_files = get_all_files_from_file_system_object_paths(
            self.paths,
            storage_interop_services_source_folder,
            ".py",
        )

        print("found these files")
        print(all_files)
        assert len(all_files) > 0
