from .consts import DataViewTypes
from .data_view import DataView
from .value_counts_view import ValueCountsView


def get_data_view_class(class_type: DataViewTypes):
    if class_type == DataViewTypes.VALUE_COUNTS:
        return ValueCountsView
    else:
        return DataView
