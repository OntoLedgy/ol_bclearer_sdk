from typing import List


def get_table_as_dictionary_column_values_as_strings(
        table_as_dictionary: dict,
        column_name: str) \
        -> List[str]:
    column_values = \
        list()

    for row_index, row_dictionary \
            in table_as_dictionary.items():
        if column_name.casefold() in row_dictionary:
            column_values.append(
                row_dictionary[column_name])

        else:
            column_values.append(
                str())

    return \
        column_values
