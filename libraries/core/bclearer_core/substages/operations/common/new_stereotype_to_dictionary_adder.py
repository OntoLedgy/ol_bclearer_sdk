from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def add_new_stereotype_to_dictionary(
    new_stereotype_dictionary: dict,
    stereotype_ea_guid: str,
    stereotype_name: str,
    stereotype_applies_to: str,
    stereotype_style: str,
) -> None:
    new_stereotype_uuid = (
        create_new_uuid()
    )

    stereotype_row_dictionary = {
        NfColumnTypes.NF_UUIDS.column_name: new_stereotype_uuid,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: stereotype_ea_guid,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: stereotype_name,
        NfEaComColumnTypes.STEREOTYPE_APPLIES_TOS.column_name: stereotype_applies_to,
        NfEaComColumnTypes.STEREOTYPE_STYLE.column_name: stereotype_style,
    }

    new_stereotype_dictionary[
        new_stereotype_uuid
    ] = stereotype_row_dictionary
