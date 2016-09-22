# -*- coding: utf-8 -*-
"""Command line interface."""
import argparse
import os
from gaaqoo import __version__, __description__
import gaaqoo.convert


def _arg_parser():
    parser = argparse.ArgumentParser(
        prog='gaaqoo',
        description=__description__)
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s version {}'.format(__version__))
    parser.add_argument('-f', '--config',
                        metavar='FILE.yml',
                        required=False,
                        help='config YAML file (default: ~/.config/gaaqoo/default.yml)')
    return parser


def main():
    """Commnad line entry point of gaaqoo."""
    args = _arg_parser().parse_args()

    conf_yaml_file = args.config if args.config else '~/.config/gaaqoo/default.yml'
    conf_yaml_file = os.path.expanduser(conf_yaml_file)
    gaaqoo.convert.main(conf_yaml_file)


if __name__ == '__main__':
    main()
