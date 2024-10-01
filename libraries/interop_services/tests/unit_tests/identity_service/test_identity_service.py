from bclearer_interop_services.delimited_text.delimited_text_read import (
    get_table_from_csv_with_header_with_encoding_detection,
)
from bclearer_orchestration_services.bclearer_load_service.hashify_and_filter.hash_creators.content_hash_column_using_all_columns_adder import (
    add_content_hash_column_using_all_columns,
)
from bclearer_orchestration_services.identification_services.b_identity_service.b_identity_universes import (
    BIdentityUniverses,
)
from bclearer_orchestration_services.identification_services.b_identity_service.initialise.b_identity_universe_initialiser import (
    initialise_b_identity_universe,
)


class TestIdentityService:
    def test_bidentity_universe_initialisation(
        self,
    ):
        bie_universe = (
            BIdentityUniverses()
        )

        initialise_b_identity_universe(
            bie_universe,
        )

        print(bie_universe)

    def test_content_hashing_using_all_columns(
        self,
        csv_file,
    ):
        custom_header = [
            "date",
            "description",
            "amount",
        ]

        table = get_table_from_csv_with_header_with_encoding_detection(
            csv_file,
            custom_header=custom_header,
        )

        add_content_hash_column_using_all_columns(
            table,
        )

        print(table)
