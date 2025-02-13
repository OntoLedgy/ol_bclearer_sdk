from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_uuidifier import (
    uuidify_dataframe,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.nf_domains.standard_object_table_column_types import (
    StandardObjectTableColumnTypes,
)
from bclearer_interop_services.file_system_service.resources_service.processes.resource_file_getter import (
    get_resource_file,
)
from pandas import DataFrame, read_csv
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.resource_constants.resource_file_constants import (
    EVOLVE_4_UNICLASS_STEREOTYPES_TYPE_OF_FILE_NAME,
)
from pipelines.uniclass.uniclass_to_nf_ea_com_source.b_code.configurations.resource_constants.resources_namespace_constants import (
    EVOLVE_4_INPUT_FOLDER_NAMESPACE,
)


def create_stereotypes_table() -> (
    DataFrame
):
    uniclass_stereotypes_table_file = get_resource_file(
        resource_namespace=EVOLVE_4_INPUT_FOLDER_NAMESPACE,
        resource_name=EVOLVE_4_UNICLASS_STEREOTYPES_TYPE_OF_FILE_NAME,
    )

    uniclass_stereotypes_table = read_csv(
        uniclass_stereotypes_table_file.absolute_path_string,
    )

    uuidified_uniclass_stereotypes_table = uuidify_dataframe(
        dataframe=uniclass_stereotypes_table,
        uuid_column_name=StandardObjectTableColumnTypes.NF_UUIDS.column_name,
    )

    return uuidified_uniclass_stereotypes_table
