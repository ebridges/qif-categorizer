from unittest.mock import patch, mock_open
from datetime import datetime
from re import compile
from qif_categorizer.qif import (
    load_qif,
    normalize_categories,
    load_categories,
    categorize_transactions,
    category_for_payee,
)


def test_load_qif():
    mock_account = "mock_account"
    mock_payee = "mock_payee"
    mock_date = "09/28/2020"
    mock_datetime = datetime.strptime(mock_date, "%m/%d/%Y")
    mock_amount = "-19.89"

    test_qif = f"!Account\nN{mock_account}\nTCCard\n^\n!Type:CCard\nC\nD{mock_date}\nNN/A\nP{mock_payee}\nT{mock_amount}\n"

    with patch("builtins.open", mock_open(read_data=test_qif)) as mock_file:
        filename = "mock_file"
        qif = load_qif(filename)
        mock_file.assert_called_with(filename)
        assert qif._accounts[0].name == mock_account
        assert qif._accounts[0].get_transactions()
        txn = qif._accounts[0].get_transactions()[0][0]
        assert txn.payee == mock_payee
        assert txn.date == mock_datetime
        assert str(txn.amount) == mock_amount


def test_load_categories():
    test_cats = r"""{
        "Cash": [{
                "payee": "^ATM WITHDRAWAL\\s+\\d{1}"
            },
            "ATM WITHDRAWAL"
        ]
    }"""

    expected_cats = {
        "Cash": [compile("^ATM WITHDRAWAL\\s+\\d{1}"), compile("ATM WITHDRAWAL")]
    }

    with patch("builtins.open", mock_open(read_data=test_cats)) as mock_file:
        filename = "mock_file"
        actual_cats = load_categories(filename)
        assert actual_cats == expected_cats
        assert actual_cats["Cash"][0].match("ATM WITHDRAWAL  8")
        assert actual_cats["Cash"][1].match("ATM WITHDRAWAL")


def test_normalize_categories():
    test_cats = {"Cash": [{"payee": "^ATM WITHDRAWAL\\s+\\d{1}"}, "ATM WITHDRAWAL"]}
    expected_cats = {"Cash": ["^ATM WITHDRAWAL\\s+\\d{1}", "ATM WITHDRAWAL"]}
    actual_cats = normalize_categories(test_cats)

    assert expected_cats == actual_cats


def test_categorize_transactions():
    mock_account = "mock_account"
    mock_payee = "mock_payee"
    mock_date = "09/28/2020"
    mock_datetime = datetime.strptime(mock_date, "%m/%d/%Y")
    mock_amount = "-19.89"
    mock_category = "MockCategory"

    test_qif = f"!Account\nN{mock_account}\nTCCard\n^\n!Type:CCard\nC\nD{mock_date}\nNN/A\nP{mock_payee}\nT{mock_amount}\n"
    mock_categories = {mock_category: [compile(mock_payee)]}

    with patch("builtins.open", mock_open(read_data=test_qif)) as mock_file:
        filename = "mock_file"
        mock_qif = load_qif(filename)
        categorize_transactions(mock_qif, mock_categories)
        txn = mock_qif._accounts[0].get_transactions()[0][0]
        assert txn.payee == mock_payee
        assert txn.category == mock_category


def test_category_for_payee():
    mock_category = "mock_category"
    mock_payee = "mock_payee"
    mock_categories = {mock_category: [compile(mock_payee)]}

    assert category_for_payee(mock_categories, mock_payee) == mock_category
