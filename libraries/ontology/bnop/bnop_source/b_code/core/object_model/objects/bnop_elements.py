from bnop_source.b_code.core.object_model.objects.bnop_objects import (
    BnopObjects,
)
from boro_common_source.ckids.boro_object_ckids import (
    BoroObjectCkIds,
)


class BnopElements(BnopObjects):

    def __init__(
        self,
        uuid,
        owning_repository_uuid,
        presentation_name=str(),
    ):
        BnopObjects.__init__(
            self,
            uuid,
            owning_repository_uuid,
            presentation_name=presentation_name,
        )

        self.add_to_registry_keyed_on_ckid_type(
            BoroObjectCkIds.Elements
        )
