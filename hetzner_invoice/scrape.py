import logging
from typing import Tuple, Any

import pyotp
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://accounts.hetzner.com/login"
POST_LOGIN_URL = "https://accounts.hetzner.com/login_check"
INVOICE_URL = "https://accounts.hetzner.com/invoice"
INVOICE_DOWNLOAD_URL = "https://accounts.hetzner.com/invoice/{invoice_number}/csv"


def get_invoice_from_hetzner_account(
    username: str, password: str, secret: str, filepath: str
) -> Tuple[str, Any]:
    s = requests.session()
    client = s.get(LOGIN_URL)
    soup = BeautifulSoup(client.content, features="html5lib")
    csrftoken = soup.find("input", dict(name="_csrf_token"))["value"]
    payload = {"_username": username, "_password": password, "_csrf_token": csrftoken}
    request_first = s.post(POST_LOGIN_URL, data=payload)
    logging.info(
        f" First step of login attempt finished with status code {request_first.status_code}."
    )
    totp = pyotp.TOTP(secret)
    request_second = s.post(LOGIN_URL, data={"_otp": totp.now()})
    logging.info(
        f" Second step of login attempt finished with status code {request_second.status_code}."
    )
    get_invoice = s.get(INVOICE_URL)
    logging.info(
        f"Last step of login attempt finished with status code {get_invoice.status_code}."
    )
    soup = BeautifulSoup(get_invoice.content, features="html5lib")

    invoice_number = (
        soup.find("span", attrs={"class": "invoice-number"}).getText().split("\n")[0]
    )

    url = INVOICE_DOWNLOAD_URL.format(invoice_number=invoice_number)
    file = s.get(url)
    logging.info(f"Downloaded most recent invoice {invoice_number}.")
    filename = filepath + "/hetzner_invoice_{invoice_number}.csv".format(
        invoice_number=invoice_number
    )
    with open(filename, "wb") as fp:
        fp.write(file.content)
    return filename, invoice_number
