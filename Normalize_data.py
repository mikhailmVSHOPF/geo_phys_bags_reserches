import numpy as np

def to_normalize_data(sublist_sorted_points):
    max_value = max(sublist_sorted_points)
    min_value = min(sublist_sorted_points)
    normal_list = np.array(
        [(item - min_value) / (max_value - min_value) for item in sublist_sorted_points])
    return normal_list, [min_value, max_value]

def to_normalize_list_data(list_sorted_points):
    normalize_data = [to_normalize_data(points)[0] for points in list_sorted_points]
    value_data = [to_normalize_data(points)[1] for points in list_sorted_points]
    return normalize_data, value_data

def to_return_list_data(sub_normalize_list, min_value, max_value):
    returned_list = [item * (max_value - min_value) + min_value for item in sub_normalize_list]
    return returned_list

def to_return_data(value, min_value, max_value):
    return value * (max_value - min_value) + min_value