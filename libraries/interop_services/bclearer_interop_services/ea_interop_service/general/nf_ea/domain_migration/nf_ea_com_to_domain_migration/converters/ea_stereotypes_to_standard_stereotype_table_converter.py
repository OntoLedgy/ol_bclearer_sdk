from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.domain_migration.common.column_name_mappings.standard_stereotype_to_nf_ea_com_column_name_bimapping import (
    get_nf_ea_com_column_name_to_standard_stereotype_dictionary,
)


def convert_ea_stereotypes_to_standard_stereotype_table(
    nf_ea_com_universe: NfEaComUniverses,
    standard_tables_dictionary: dict,
) -> dict:
    ea_stereotypes = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_STEREOTYPES
    ]

    standard_stereotype_table_renaming_dictionary = (
        get_nf_ea_com_column_name_to_standard_stereotype_dictionary()
    )

    nf_ea_com_table_filtered_and_renamed = dataframe_filter_and_rename(
        dataframe=ea_stereotypes,
        filter_and_rename_dictionary=standard_stereotype_table_renaming_dictionary,
    )

    standard_tables_dictionary[
        NfEaComCollectionTypes.EA_STEREOTYPES.collection_name
    ] = nf_ea_com_table_filtered_and_renamed

    return standard_tables_dictionary
