# -*- coding: utf-8 -*-
"""
Cmd line parser
"""

import argparse
import sys

import finder
from finder.server import cmd_http_server

__author__ = "hyxf"
__version__ = "1.0.0"


def execute():
    """
    Program entry point
    :return:
    """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser(prog='finder', description='LAN file sharing {0}'.format(finder.__version__),
                                     epilog='make it easy')

    parser.set_defaults(func=cmd_http_server)
    parser.add_argument('-i', '--ip', type=str, help='Local IP')
    parser.add_argument('-p', '--port', type=int, default=8000, help='Local port')
    parser.add_argument('-d', '--dir', type=str, help='Shared directory path')
    parser.add_argument('-q', '--qr', action='store_true', default=False, help='Show QRCode')
    parser.add_argument('-u', '--upload', action='store_true', default=False, help='Support upload')

    parser.add_argument('--start', action='store_true', default=False, help='daemon start')
    parser.add_argument('--pid_file', type=str, default='/var/run/finder.pid', help='pid_file')
    parser.add_argument('--log_file', type=str, default='/var/log/finder.log', help='log_file')
    parser.add_argument('--stop', action='store_true', default=False, help='daemon stop')

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    """
    test main
    """
    # sys.argv.append('-q')
    # sys.argv.append('--start')
    execute()
