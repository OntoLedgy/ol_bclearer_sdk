from bclearer_core.substages.operations.common.classifier_adder import (
    add_new_classifier_to_dictionary,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)


def add_new_association_class_to_dictionary(
    new_classifier_dictionary: dict,
    package_nf_uuid: str,
) -> str:
    association_class_nf_uuid = add_new_classifier_to_dictionary(
        new_classifier_dictionary=new_classifier_dictionary,
        package_nf_uuid=package_nf_uuid,
        ea_element_type=EaElementTypes.ASSOCIATION,
    )

    return association_class_nf_uuid
