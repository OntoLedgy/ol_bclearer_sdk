from bnop.core.object_model.objects.bnop_objects import (
    BnopObjects,
)
from boro_common_source.ckids.place_number_type_ckids import (
    PlaceNumberTypeCkIds,
)


class BnopPlacedObjectsDictionaries(
    object
):

    def __init__(self):
        self.relation_placed_object_dictionary = (
            {}
        )

    def add_tuple_placed_object_to_dictionary(
        self,
        placing_ckid: PlaceNumberTypeCkIds,
        relation_placed_object: BnopObjects,
    ):
        self.relation_placed_object_dictionary[
            placing_ckid
        ] = relation_placed_object

    def try_get_relation_placed_object_for_place_number_ckid(
        self,
        placing_ckid: PlaceNumberTypeCkIds,
    ):
        relation_placed_object = self.relation_placed_object_dictionary[
            placing_ckid
        ]

        return relation_placed_object
