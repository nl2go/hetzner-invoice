import pyotp
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://accounts.hetzner.com/login"
POST_LOGIN_URL = "https://accounts.hetzner.com/login_check"
INVOICE_URL = "https://accounts.hetzner.com/invoice"
INVOICE_DOWNLOAD_URL = "https://accounts.hetzner.com/invoice/{invoice_number}/csv"


def get_invoice_from_hetzner_account(
    username: str, password: str, secret: str, filepath: str
) -> str:
    s = requests.session()
    client = s.get(LOGIN_URL)
    soup = BeautifulSoup(client.content, features="html5lib")
    csrftoken = soup.find("input", dict(name="_csrf_token"))["value"]
    payload = {"_username": username, "_password": password, "_csrf_token": csrftoken}

    s.post(POST_LOGIN_URL, data=payload)
    totp = pyotp.TOTP(secret)
    s.post(LOGIN_URL, data={"_otp": totp.now()})
    get_invoice = s.get(INVOICE_URL)
    soup = BeautifulSoup(get_invoice.content, features="html5lib")

    invoice_number = (
        soup.find("span", attrs={"class": "invoice-number"}).getText().split("\n")[0]
    )

    url = INVOICE_DOWNLOAD_URL.format(invoice_number=invoice_number)
    file = s.get(url)
    filename = filepath + "/hetzner_invoice_{invoice_number}.csv".format(
        invoice_number=invoice_number
    )
    with open(filename, "wb") as fp:
        fp.write(file.content)
    return filename
