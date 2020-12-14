from os.path import basename
from sys import argv
from argparse import ArgumentParser
from logging import basicConfig, DEBUG, INFO, info

from qif_categorizer.categorizer_ui import CategorizerUIApp
from qif_categorizer.qif import (
    load_qif,
    load_categories,
    categorize_transactions,
    uncategorized_txns,
)


def run_manual_categorization(uncategorized, cats):
    ui = CategorizerUIApp()
    ui.transaction_list = uncategorized
    ui.run()


def run_categorization(qif_file, cat_file):
    qif = load_qif(qif_file)
    cats = load_categories(cat_file)
    categorize_transactions(qif, cats)
    uncategorized = uncategorized_txns(qif)
    print([str(t) for t in uncategorized])

    if len(uncategorized) > 0:
        run_manual_categorization(uncategorized, cats)


def configure_logging(verbose):
    if verbose:
        level = DEBUG
    else:
        level = INFO

    basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        level=level,
    )


def run():
    parser = ArgumentParser(prog=basename(argv[0]))
    parser.add_argument('-v', '--verbose', default=False, action='store_true')
    parser.add_argument(
        '-q', '--qif-file', required=True, help='QIF File to categorize.'
    )
    parser.add_argument(
        '-c', '--categories', required=True, help='Category patterns file.'
    )
    args = parser.parse_args()

    configure_logging(args.verbose)

    qif_file = args.qif_file
    categories = args.categories

    info(
        f'''{parser.prog} called:
        QIF File: {qif_file}
        Category file: {categories}'''
    )

    run_categorization(qif_file, categories)


if __name__ == '__main__':
    run()
