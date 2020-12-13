from json import load
from qifparse.parser import QifParser
from re import compile
from copy import deepcopy


def load_qif(qif_file):
    if qif_file:
        with open(qif_file) as f:
            qif = QifParser.parse(f)
            if len(qif._accounts) > 0:
                return qif


def save_qif(qif, qif_file):
    with open(qif_file, 'w') as f:
        f.write(str(qif))


def load_categories(cat_file):
    if cat_file:
        with open(cat_file) as f:
            categories = load(f)
            categories = normalize_categories(categories)
            for key in categories:
                for idx in range(len(categories[key])):
                    categories[key][idx] = compile(categories[key][idx])
            return categories


def normalize_categories(c):
    cats = deepcopy(c)
    for key in cats:
        categories = cats[key]
        for i in range(len(categories)):
            if type(categories[i]) == dict:
                categories[i] = categories[i]['payee']
    return cats


def categorize_transactions(qif, categories):
    txns = qif._accounts[0].get_transactions()[0]
    for txn in txns:
        payee = txn.payee
        category = category_for_payee(categories, payee)
        if category:
            txn.category = category


def category_for_payee(categories, payee):
    for category in categories:
        for regex in categories[category]:
            if regex.match(payee):
                return category
