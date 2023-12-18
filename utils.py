from collections import OrderedDict


def remove_duplicates(input_list):
    seen = OrderedDict.fromkeys(input_list)

    result = list(seen.keys())

    return result
