from pandas import DataFrame
from nf_common.code.services.identification_services.pandas_null_values.pandas_null_value_swap_between_types import PandasNullValueSwapBetweenTypes


def swap_between_pandas_null_values_in_dataframe(
        dataframe: DataFrame,
        pandas_null_value_swap_between_type: PandasNullValueSwapBetweenTypes) \
        -> None:
    from_pandas_null_value = \
        pandas_null_value_swap_between_type.from_pandas_null_value

    to_pandas_null_value = \
        pandas_null_value_swap_between_type.to_pandas_null_value

    dataframe.replace(
        from_pandas_null_value.value,
        to_pandas_null_value.value,
        inplace=True)
