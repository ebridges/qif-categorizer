from sys import argv
from argparse import ArgumentParser
from logging import basicConfig, DEBUG, INFO, info

from qif_categorizer.qif import (
    load_qif,
    load_categories,
    categorize_transactions,
)


def run_categorization(qif_file, cat_file):
    qif = load_qif(qif_file)
    cats = load_categories(cat_file)
    categorize_transactions(qif, cats)
    print(str(qif))


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


if __name__ == '__main__':
    parser = ArgumentParser(prog=argv[0])
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
        f'''{args.prog} called:
        QIF File: {qif_file}
        Category file: {categories}'''
    )

    run_categorization(qif_file, categories)
