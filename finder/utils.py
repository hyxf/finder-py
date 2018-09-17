# -*- coding: utf-8 -*-
import os
import socket
import time

import qrcode


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


def get_file_time(file):
    """
    get file time

    :param file:
    :return:
    """
    file_stat = os.stat(file)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_stat.st_mtime))


def get_file_size(file):
    """
    get file size

    :param file:
    :return:
    """
    file_stat = os.stat(file)
    size = file_stat.st_size
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


def get_home():
    """
    get user home
    :return:
    """
    home = os.path.expanduser('~')
    if home:
        return home
    home = os.path.expandvars('$HOME')
    if home:
        return home
    home = os.environ['HOME']
    if home:
        return home
    else:
        return None


def get_log():
    """
    get log file
    :return:
    """
    home = get_home()
    if home:
        finder_home = os.path.join(home, '.finder-py')
        if not os.path.exists(finder_home):
            os.mkdir(finder_home)
        return os.path.join(finder_home, 'finder.log')
    else:
        return '/var/log/finder.log'


def get_pid():
    """
    get pid file
    :return:
    """
    home = get_home()
    if home:
        finder_home = os.path.join(home, '.finder-py')
        if not os.path.exists(finder_home):
            os.mkdir(finder_home)
        return os.path.join(finder_home, 'finder.pid')
    else:
        return '/var/run/finder.pid'
