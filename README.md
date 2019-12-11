[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://travis-ci.com/nl2go/hetzner-invoice.svg?branch=master)](https://travis-ci.com/nl2go/hetzner-invoice)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/hetzner-invoice)](https://codecov.io/gh/nl2go/hetzner-invoice)

# hetzner-invoice
Automatically download and transform Hetzner invoices.

To install the dependencies, run 
`pip install poetry` and then `poetry install`.

In Ubuntu 18.04 you may have to install `python-pip`.

# How to run the software

## Running tests

You can run tests with:

```
  poetry run python -m pytest --cov=invoice tests/
```

### Contributing
To install the [pre-commit hook](https://pre-commit.com), run `pip install pre-commit` and then `pre-commit install`.