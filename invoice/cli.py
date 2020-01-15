import click
import pandas as pd

from invoice.load_data import read_invoice_file, read_server_info_file
from invoice.process_invoice import populate_columns
from invoice.scraper import get_invoice_from_hetzner_account


@click.command()
@click.option("--user", help="Hetzner Account Username.", type=str)
@click.option("--pw", help="Hetzner Account Password.", type=str)
@click.option("--secret", help="Hetzner Account Base Secret.", type=str)
@click.option("--filepath", help="Where invoice file will be saved.", type=str)
def load_transform_invoice(user, pw, secret, filepath) -> pd.DataFrame:
    """Automatically download and transform most recent Hetzner invoice"""
    invoice_filepath = get_invoice_from_hetzner_account(user, pw, secret, filepath)
    invoice_data = read_invoice_file(invoice_filepath)
    server_data = read_server_info_file("hetzner-invoice/server_types.json")
    result = populate_columns(invoice_data, server_data)
    return result


if __name__ == "__main__":
    load_transform_invoice()
