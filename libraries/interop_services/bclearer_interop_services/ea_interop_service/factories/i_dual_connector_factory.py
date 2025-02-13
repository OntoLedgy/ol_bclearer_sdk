from bclearer_interop_services.ea_interop_service.i_dual_objects.connectors.i_dual_connector import (
    IDualConnector,
)
from bclearer_interop_services.ea_interop_service.i_dual_objects.elements.i_dual_element import (
    IDualElement,
)


def create_i_dual_connector(
    child_object: IDualElement,
    parent_object: IDualElement,
    connector_name: str,
    connector_type: str,
    ea_object_note: str,
    ea_connector_stereotype_ex: str,
) -> IDualConnector:
    if connector_name is None:
        ea_object_name = ""

    else:
        ea_object_name = connector_name

    i_dual_connector = IDualConnector(
        child_object.connectors.add_new(
            ea_object_name=ea_object_name,
            ea_object_type=connector_type,
        )
    )

    i_dual_connector.notes = (
        ea_object_note
    )

    i_dual_connector.supplier_id = (
        parent_object.element_id
    )

    i_dual_connector.client_id = (
        child_object.element_id
    )

    # TODO: Send in as enum
    hard_coded_direction = (
        "Source -> Destination"
    )

    i_dual_connector.direction = (
        hard_coded_direction
    )

    if (
        len(ea_connector_stereotype_ex)
        > 0
    ):
        i_dual_connector.stereotype_ex = (
            ea_connector_stereotype_ex
        )

    i_dual_connector.update()

    child_object.connectors.refresh()

    return i_dual_connector
