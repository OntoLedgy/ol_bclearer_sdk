from bnop_source.b_code.core.object_model.objects.bnop_objects import (
    BnopObjects,
)
from bnop_source.b_code.migrations.bnop_to_xml_migration.xml_bnop_registers import (
    XmlBnopRegisters,
)
from boro_common_source.ckids.boro_object_ckids import (
    BoroObjectCkIds,
)


def sort_names_by_named_objects():
    sorted_bnop_names = list()

    for (
        bnop_object_uuid,
        bnop_object,
    ) in (
        BnopObjects.registry_keyed_on_uuid.items()
    ):
        for (
            bnop_name
        ) in bnop_object.is_named_bys:
            sorted_bnop_names.append(
                bnop_name
            )

    XmlBnopRegisters.update_migration_uow(
        boro_ckid_type=BoroObjectCkIds.Names,
        bnop_objects=sorted_bnop_names,
    )
