import logging
import os

from hetzner_invoice.invoice import (
    load_transform_invoice,
    save_invoice_to_db,
    transform_invoice_df,
)

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

invoice_data = load_transform_invoice(
    user=os.getenv("HETZNER_INVOICE_ACCOUNT_USER"),
    pw=os.getenv("HETZNER_INVOICE_ACCOUNT_PW"),
    secret=os.getenv("HETZNER_INVOICE_ACCOUNT_2FA_SECRET"),
    filepath=os.getenv("HETZNER_INVOICE_DIR"),
)

invoice_data = transform_invoice_df(invoice_data)

save_invoice_to_db(
    data=invoice_data,
    user=os.getenv("HETZNER_INVOICE_DB_USER"),
    pw=os.getenv("HETZNER_INVOICE_DB_PW"),
    host=os.getenv("HETZNER_INVOICE_DB_HOST"),
    port=os.getenv("HETZNER_INVOICE_DB_PORT"),
    schema=os.getenv("HETZNER_INVOICE_DB_SCHEMA"),
)
