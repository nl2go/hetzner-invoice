import logging
from typing import List, Tuple

import mysql.connector
from pandas import DataFrame

from hetzner_invoice.combine import populate_columns
from hetzner_invoice.load import read_invoice_file, read_server_info_file
from hetzner_invoice.scrape import get_invoice_from_hetzner_account


def load_transform_invoice(user: str, pw: str, secret: str, filepath: str) -> DataFrame:
    """
    Downloads and transforms data from the most recent Hetzner invoice.
    :param user: Username for the Hetzner Account
    :param pw: Password for the Hetzner Account
    :param secret: Base secret for the Hetzner Account
    :param filepath: Path where invoice data will be saved
    :return: DataFrame augmented with additional information
    """
    invoice_filepath, invoice_nr = get_invoice_from_hetzner_account(
        user, pw, secret, filepath
    )
    data = read_invoice_file(invoice_filepath)
    server_data = read_server_info_file("server_types.json")
    result_df = populate_columns(data, server_data, invoice_nr)
    logging.info(
        f"Created DataFrame from invoice and server data. Result has {result_df.shape[0]} rows and {result_df.shape[1]} columns. "
    )
    return result_df


def transform_invoice_df(invoice_df: DataFrame) -> Tuple[List[tuple], list]:
    columns = list(invoice_df.columns)
    result_list = invoice_df.values.tolist()
    record_data = []
    for entry in result_list:
        record_data.append(tuple(entry))
    return record_data, columns


def save_invoice_to_db(
    data: List, columns: List, user: str, pw: str, host: str, port: str, schema: str
):
    """
    Downloads and transforms data from the most recent Hetzner invoice.
    :param data: List with the transformed invoice data
    :param columns: List with column names
    :param user: Username for the database
    :param pw: Password for the database
    :param host: Database host
    :param port: Database port
    :param schema: Database schema
    """
    logging.info("Connecting to the database")
    try:
        cnx = mysql.connector.connect(
            user=user, password=pw, host=host, port=port, database=schema
        )
        mysql.connector.conversion.MySQLConverter._timestamp_to_mysql = (
            mysql.connector.conversion.MySQLConverter._datetime_to_mysql
        )
    except mysql.connector.Error as err:
        logging.error(f"Error when trying to connect to database: {err}")
    else:
        cursor = cnx.cursor()
        search_duplicate = (
            "SELECT * FROM invoices WHERE type = %s AND description = %s AND id "
            "= %s AND invoice_nr = %s "
        )
        update_record = (
            "UPDATE invoices SET start_date = %s, end_date = %s, quantity = %s, price= %s, last_updated "
            "= %s WHERE type = %s AND description = %s AND id "
            "= %s AND invoice_nr = % "
        )
        insert_record = (
            "INSERT INTO invoices "
            "(type, description, start_date, end_date, quantity, unit_price, price, cores, memory, disk, "
            "price_monthly, role, id, environment, invoice_nr, last_updated) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        for i in range(0, len(data)):
            record = data[i]
            record_type, record_description, start_date, end_date, quantity, price, last_updated, record_id, record_invoice_nr = (
                record[columns.index("type")],
                record[columns.index("description")],
                record[columns.index("start_date")],
                record[columns.index("end_date")],
                record[columns.index("quantity")],
                record[columns.index("price")],
                record[columns.index("last_updated")],
                record[columns.index("id")],
                record[columns.index("invoice_nr")],
            )

            cursor.execute(
                search_duplicate,
                (record_type, record_description, record_id, record_invoice_nr),
            )
            result = cursor.fetchone()
            if result:
                logging.info(
                    f"This record already exists in the database: {record_type}, {record_description}, {record_id}, "
                    f"{record_invoice_nr}, updating it "
                )
                cursor.execute(
                    update_record,
                    (
                        start_date,
                        end_date,
                        quantity,
                        price,
                        last_updated,
                        record_type,
                        record_description,
                        record_id,
                        record_invoice_nr,
                    ),
                )
            else:
                logging.info(f"No records found. Inserting new record")
                cursor.execute(insert_record, data[i])

        cnx.commit()

        cursor.close()
        cnx.close()
