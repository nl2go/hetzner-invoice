import json
from typing import List

import pandas as pd


def read_invoice_file(filepath: str) -> pd.DataFrame:
    """
    Reads a csv file with the specified path, transforms it into a DataFrame adding column names.
    :param filepath: File path of the invoice.
    :return: DataFrame with named columns.
    """
    invoice_df = pd.read_csv(
        filepath,
        names=[
            "type",
            "description",
            "start_date",
            "end_date",
            "quantity",
            "unit_price",
            "price",
        ],
        index_col=False,
    )
    return invoice_df


def read_server_info_file(filepath: str) -> List:
    """
    Loads information in a json file containing server properties. That data is available via the Hetzner API.
    :param filepath: File path of the json file.
    :return: List containing information on all available server types.
    """
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    server_types_data = data.get("server_types")
    return server_types_data
