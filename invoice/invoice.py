import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

from invoice.load import read_invoice_file, read_server_info_file
from invoice.combine import populate_columns
from invoice.scrape import get_invoice_from_hetzner_account


def load_transform_invoice(user: str, pw: str, secret: str, filepath: str) -> DataFrame:
    """
    Downloads and transforms data from the most recent Hetzner invoice.
    :param user: Username for the Hetzner Account
    :param pw: Password for the Hetzner Account
    :param secret: Base secret for the Hetzner Account
    :param filepath: Path where invoice data will be saved
    :return: DataFrame augmented with additional information
    """
    invoice_filepath = get_invoice_from_hetzner_account(user, pw, secret, filepath)
    data = read_invoice_file(invoice_filepath)
    server_data = read_server_info_file("server_types.json")
    result_df = populate_columns(data, server_data)
    return result_df


def save_invoice_to_db(
    data: pd.DataFrame, user: str, pw: str, host: str, port: str, schema: str
):
    """
    Downloads and transforms data from the most recent Hetzner invoice.
    :param data: Dataframe with the transformed invoice data
    :param user: Username for the database
    :param pw: Password for the database
    :param host: Database host
    :param port: Database port
    :param schema: Database schema
    """
    db_url = "mysql+pymysql://{user}:{pw}@{host}:{port}/{schema}".format(
        user=user, pw=pw, host=host, port=port, schema=schema
    )
    engine = create_engine(db_url, echo=False)
    data.to_sql(name="invoices", con=engine, if_exists="append", index=False)
