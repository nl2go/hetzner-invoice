import re
from datetime import datetime
from typing import List, Optional

import pandas as pd
from cafeteria.patterns import dict

ROLE_OPTIONS = ["db-", "app-", "mta-", "api-"]
ENVIRONMENT_OPTIONS = ["-prod-", "-dev-", "-staging-", "-test-"]


def get_matching_option(options: List, data: str) -> Optional[str]:
    """
    Extracts the environment or role matching one of those defined in a list.
    :param options: List of available environments or roles.
    :param data: Input data.
    :return: First string matching any of those in the options.
    """
    matches = next((x for x in options if x in data), None)
    if matches:
        return matches.strip("-")
    else:
        return None


def get_server_id(data: str) -> Optional[int]:
    """
    Extracts six digit id of server.
    :param data: Input data.
    :return: Server id number.
    """
    server_id = re.findall(r"#(\d{6})", data)
    if server_id:
        return int(server_id[0])
    else:
        return None


def get_server_type(data: str) -> Optional[str]:
    """
    Extracts type of the server.
    :param data: Input data.
    :return: First regex match.
    """
    server_type = re.findall(r"(cx.*)", data)
    if server_type:
        return server_type[0]
    else:
        return None


def get_server_information(
    server_name: str, server_data: List, key: str
) -> Optional[str]:
    """
    Extracts information on server cores, disk, memory and price.
    :param server_name: Name of the server.
    :param server_data: Input server data.
    :param key: Key of the server information inside server data.
    :return:
    """
    if server_name:
        idx = [x.get("name") for x in server_data].index(server_name)
        if key == "prices":
            return dict.get_by_path(server_data[idx][key][0], "price_monthly", "gross")
        else:
            return server_data[idx][key]
    else:
        return None


def populate_columns(
    invoice_df: pd.DataFrame, server_types_data: List, invoice_nr: str
) -> pd.DataFrame:
    """
    Populates additional columns with complementary information.
    :param server_types_data: Dataset with server properties
    :param invoice_df: Original Hetzner invoice data
    :param invoice_nr: Number of the invoice generated by Hetzner
    :return: DataFrame augmented with additional information
    """
    server = [get_server_id(x) for x in invoice_df["description"]]

    environment = [
        get_matching_option(ENVIRONMENT_OPTIONS, x) for x in invoice_df["description"]
    ]
    role = [get_matching_option(ROLE_OPTIONS, x) for x in invoice_df["description"]]

    server_type = [get_server_type(x) for x in invoice_df["type"]]

    for key in ["cores", "memory", "disk", "prices"]:
        invoice_df[key] = [
            str(get_server_information(x, server_types_data, key)) for x in server_type
        ]
    invoice_df = (
        invoice_df.assign(role=role, id=server, environment=environment)
        .rename(columns={"prices": "price_monthly"})
        .replace({"None": None})
    )

    invoice_df["invoice_nr"] = invoice_nr
    invoice_df["last_updated"] = datetime.utcnow()
    invoice_df = invoice_df.where(pd.notnull(invoice_df), None)
    return invoice_df
