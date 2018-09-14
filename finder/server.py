# -*- coding: utf-8 -*-
import os

from flask import Flask

from finder import daemon
from finder import utils

app = Flask(__name__, static_folder='static', template_folder='templates')

www = os.getcwd()


@app.route('/')
def index():
    return 'hello'


@app.route('/<path:path>')
def index_path(path):
    return path


# --------------------------------------------

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
        www = args.dir

    app.run(host=ip, port=args.port)
