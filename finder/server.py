# -*- coding: utf-8 -*-
import os

from finder import daemon
from finder import utils


def cmd_http_server(args):
    """
    http server
    :param args:
    :return:
    """
    if args.stop:
        daemon.daemon_exec(command='stop',
                           log_file=args.log_file,
                           pid_file=args.pid_file)
    if args.ip:
        ip = args.ip
    else:
        ip = utils.get_ip()

    if args.dir:
        base_dir = args.dir
    else:
        base_dir = os.getcwd()
    pass
