def filter_none_values(data: dict) -> dict:
    """
    Filters out keys from the dictionary where the value is None or null.

    Args:
        data (dict): The dictionary to filter.

    Returns:
        dict: A new dictionary with None values removed.
    """
    return {key: value for key, value in data.items() if value is not None}
