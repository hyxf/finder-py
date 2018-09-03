# -*- coding: utf-8 -*-

import os
import socket
import sys
from os import path

import qrcode

from finder.server import daemon

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


def qr_code_show(message):
    """
    show qr code
    :param message:
    :return:
    """
    if message:
        try:
            qr = qrcode.make(message)
            qr.get_image().show()
        except Exception as e:
            print(e)


def _index_format():
    """
    index.html format

    :rtype: str
    :return:
    """
    index_path = path.join(path.dirname(__file__), 'index.html')
    index_file = open(index_path)
    try:
        html_list = [x for x in index_file.readlines()]
        content = "".join(html_list)
    finally:
        index_file.close()
    return content


def index_content(request_path, table_content, cli_name='GUtils', support_upload=False):
    """
    index.html content

    :param request_path:
    :param table_content:
    :param cli_name:
    :param support_upload:
    :rtype: str
    :return:
    """
    if support_upload:
        style = ''
    else:
        style = 'utils-hidden'
    return _index_format() \
        .replace('{cli_name}', cli_name) \
        .replace('{request_path}', request_path) \
        .replace('{table_content}', table_content) \
        .replace('{support_upload}', style)


def table_tr(file_href, file_title, file_time, file_size='-'):
    """
    table tr

    :param file_href:
    :param file_title:
    :param file_time:
    :param file_size:
    :rtype: str
    :return:
    """
    tr_format = '<tr><td><a href="{0}" title="{1}">{1}</a> </td><td>{2}</td><td>{3}</td></tr>'
    return tr_format.format(file_href, file_title, file_time, file_size)


def convert_file_size(size):
    """
    convert file size

    :param size:
    :return:
    """
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    if size >= gb:
        return "{:.2f} GB".format(size / gb)
    elif size >= mb:
        return "{:.2f} MB".format(size / mb)
    elif size >= kb:
        return "{:.2f} KB".format(size / kb)
    else:
        return "{:d} B".format(size)


def get_ip():
    """
    get local ip
    :return:
    """
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return '127.0.0.1'


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
        ip = get_ip()

    if args.dir:
        base_dir = args.dir
    else:
        base_dir = os.getcwd()
    if is_py3:
        import finder.server.httpserver
        httpserver.run_server(bind=ip,
                              port=args.port,
                              base_dir=base_dir,
                              show_qr=args.qr,
                              support_upload=args.upload,
                              daemon_start=args.start,
                              pid_file=args.pid_file,
                              log_file=args.log_file)
    elif is_py2:
        import finder.server.httpserver27
        httpserver27.run_server(bind=ip,
                                port=args.port,
                                base_dir=base_dir,
                                show_qr=args.qr,
                                support_upload=args.upload,
                                daemon_start=args.start,
                                pid_file=args.pid_file,
                                log_file=args.log_file)
    else:
        print('not support python version')
