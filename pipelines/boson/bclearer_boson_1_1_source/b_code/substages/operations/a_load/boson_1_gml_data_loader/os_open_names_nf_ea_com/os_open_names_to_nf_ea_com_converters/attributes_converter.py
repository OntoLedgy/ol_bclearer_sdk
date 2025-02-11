from bclearer_core.common_knowledge.matched_objects import (
    MatchedEaObjects,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_interop_services.dataframe_service.dataframe_helpers.dataframe_filter_and_renamer import (
    dataframe_filter_and_rename,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.processes.dataframes.nf_ea_com_table_appender import (
    append_nf_ea_com_table,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def convert_to_attributes(
    os_open_names_dictionary: dict,
    nf_ea_com_universe: NfEaComUniverses,
    attribute_name: str,
    initial_value_column_name: str,
    os_open_names_table_name: str,
    matched_classifying_ea_classifier: MatchedEaObjects = None,
) -> NfEaComUniverses:
    os_open_names = (
        os_open_names_dictionary[
            os_open_names_table_name
        ]
    )

    log_message(
        message="adding "
        + str(os_open_names.shape[0])
        + " in "
        + os_open_names_table_name
        + ":"
        + attribute_name
        + " to EA Attributes"
    )

    new_ea_attributes = __create_new_ea_attributes(
        os_open_names=os_open_names,
        nf_ea_com_universe=nf_ea_com_universe,
        attribute_name=attribute_name,
        initial_value_column_name=initial_value_column_name,
        matched_classifying_ea_classifier=matched_classifying_ea_classifier,
    )

    nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections = append_nf_ea_com_table(
        nf_ea_com_dictionary=nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections,
        new_nf_ea_com_collection=new_ea_attributes,
        nf_ea_com_collection_type=NfEaComCollectionTypes.EA_ATTRIBUTES,
    )

    return nf_ea_com_universe


def __create_new_ea_attributes(
    os_open_names: DataFrame,
    nf_ea_com_universe: NfEaComUniverses,
    attribute_name: str,
    initial_value_column_name: str,
    matched_classifying_ea_classifier: MatchedEaObjects = None,
) -> DataFrame:
    if (
        matched_classifying_ea_classifier
        is None
    ):
        classifying_ea_classifier_id = 0

        classifying_ea_classifier_name = (
            "CharacterString"
        )

    else:
        ea_classifiers = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ]

        classifying_ea_classifier_id = ea_classifiers.at[
            ea_classifiers[
                NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
            ]
            .eq(
                matched_classifying_ea_classifier.ea_guid
            )
            .idxmax(),
            NfColumnTypes.NF_UUIDS.column_name,
        ]

        classifying_ea_classifier_name = (
            None
        )

    filter_and_rename_dictionary = {
        NfColumnTypes.NF_UUIDS.column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_CONTAINING_EA_CLASSIFIER.column_name,
        initial_value_column_name: NfEaComColumnTypes.ELEMENT_COMPONENTS_DEFAULT.column_name,
    }

    new_ea_attributes = dataframe_filter_and_rename(
        dataframe=os_open_names,
        filter_and_rename_dictionary=filter_and_rename_dictionary,
    )

    new_ea_attributes[
        NfColumnTypes.NF_UUIDS.column_name
    ] = create_new_uuid()

    new_ea_attributes[
        NfEaComColumnTypes.ELEMENT_COMPONENTS_CLASSIFYING_EA_CLASSIFIER.column_name
    ] = classifying_ea_classifier_id

    new_ea_attributes[
        NfEaComColumnTypes.ELEMENT_COMPONENTS_UML_VISIBILITY_KIND.column_name
    ] = "Public"

    new_ea_attributes[
        NfEaComColumnTypes.ELEMENT_COMPONENTS_TYPE.column_name
    ] = classifying_ea_classifier_name

    new_ea_attributes[
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name
    ] = attribute_name

    return new_ea_attributes
