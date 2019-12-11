import json

import pandas as pd
import pytest

from invoice.invoice import populate_columns
from invoice.load_data import read_invoice_file, read_server_info_file
from invoice.values import COLNAMES


@pytest.fixture
def invoice_data():
    return pd.read_csv(r"tests/invoice.csv", names=COLNAMES, index_col=False)


@pytest.fixture
def server_info_data():
    return read_server_info_file(r"server_types.json")


@pytest.fixture
def invoice_complete():
    return pd.read_csv(r"tests/invoice_complete.csv", index_col=False).replace(
        {"None": None}
    )


def test_read_invoice_data(invoice_data):
    invoice_df = read_invoice_file(r"tests/invoice.csv")
    assert invoice_df.equals(invoice_data)
    assert list(invoice_df.columns) == list(invoice_data.columns)


def test_read_server_info_data(server_info_data):
    with open("server_types.json", "r") as read_file:
        data = json.load(read_file)
    server_data = data.get("server_types")
    assert server_data == server_info_data


def test_populate_columns(invoice_data, server_info_data, invoice_complete):
    res_df = populate_columns(
        invoice_df=invoice_data, server_types_data=server_info_data
    )
    assert res_df.sort_index(axis=1).equals(invoice_complete.sort_index(axis=1))
