# -*- coding: utf-8 -*-
"""
Cmd line parser
"""

import argparse
import sys

import finder
from finder import utils
from finder.server import cmd_http_server

__author__ = "hyxf"
__version__ = "1.0.0"


def execute():
    """
    Program entry point
    :return:
    """
    parser = argparse.ArgumentParser(prog='finder', description='LAN file sharing {0}'.format(finder.__version__),
                                     epilog='make it easy')

    parser.set_defaults(func=cmd_http_server)
    parser.add_argument('-i', '--ip', type=str, help='Local IP')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Local port')
    parser.add_argument('-d', '--dir', type=str, help='Shared directory path')

    parser.add_argument('-q', '--qr', action='store_true', default=False, help='Show QRCode')
    parser.add_argument('-u', '--upload', action='store_true', default=False, help='Support upload')
    parser.add_argument('-m', '--mkdir', action='store_true', default=False, help='Support mkdir')
    parser.add_argument('-z', '--zip', action='store_true', default=False, help='Support zip')

    parser.add_argument('-r', '--rm', action='store_true', default=False, help='Support rm')

    parser.add_argument('--hidden', action='store_true', default=False, help='Show hidden')

    parser.add_argument('--user', type=str, help='Basic Auth User')
    parser.add_argument('--password', type=str, help='Basic Auth Password')

    parser.add_argument('--start', action='store_true', default=False, help='daemon start')
    parser.add_argument('--stop', action='store_true', default=False, help='daemon stop')
    parser.add_argument('--pid_file', type=str, default=utils.get_pid(), help='pid_file')
    parser.add_argument('--log_file', type=str, default=utils.get_log(), help='log_file')

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    """
    test main
    """
    # sys.argv.append('--user')
    # sys.argv.append('admin')
    # sys.argv.append('--password')
    # sys.argv.append('pass')

    # sys.argv.append('--hidden')
    # sys.argv.append('-r')
    sys.argv.append('-u')
    sys.argv.append('-m')
    sys.argv.append('--zip')

    sys.argv.append('-d')
    sys.argv.append(utils.get_home())
    execute()
