[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://travis-ci.com/nl2go/hetzner-invoice.svg?branch=master)](https://travis-ci.com/nl2go/hetzner-invoice)
[![Codecov](https://codecov.io/gh/nl2go/hetzner-invoice/branch/master/graphs/badge.svg)](https://codecov.io/gh/nl2go/hetzner-invoice)

# hetzner-invoice
Automatically download and transform Hetzner invoices.

## What is it?
This tool is intended to help analyze Hetzner invoices with regards to cost distribution between different 
products used as well as infrastructure cost over time, in an automated way.
 The [Hetzner website](https://www.hetzner.de/) (to date) does not provide any means for that.
 
## Quick Start
**Dependencies:**
- docker-compose

Clone the project and edit the `docker-compose.yml` file to contain your credentials of your Hetzner account.
```
HETZNER_INVOICE_ACCOUNT_USER: <insert your username>
HETZNER_INVOICE_ACCOUNT_PW: <insert your password>
HETZNER_INVOICE_ACCOUNT_2FA_SECRET: <insert your 2FA secret>
```

Now, running `docker-compose run app` will trigger the following:
1) Scraping the Hetzner website for the last invoice in your account
2) Downloading latest invoice and augmenting it with some more info
3) Saving the data to a database.


### Contributing
To install the [pre-commit hook](https://pre-commit.com), run `pip install pre-commit` and then `pre-commit install`.