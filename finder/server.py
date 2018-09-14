# -*- coding: utf-8 -*-
import os

from flask import Flask, abort, send_file
from flask import render_template

from finder import daemon
from finder import utils

app = Flask(__name__, static_folder='static', template_folder='templates')

key_www = 'www'


def _ls(path, show_hidden=True):
    www = app.config.get(key_www)
    lists = os.listdir(path)
    if not show_hidden:
        lists = [x for x in lists if not x.startswith('.')]
    files = []
    for file_name in lists:
        file_path = os.path.join(path, file_name)
        file_map = {'path': file_path.replace(www, ''),
                    'name': file_name,
                    'time': utils.get_file_time(file_path),
                    'size': utils.get_file_size(file_path)}
        files.append(file_map)
    return files


@app.route('/', methods=['GET'])
def index():
    www = app.config.get(key_www)
    files = _ls(www, show_hidden=False)
    return render_template('index.html',
                           title='Finder',
                           files=files)


@app.route('/<path:path>', methods=['GET'])
def index_path(path):
    www = app.config.get(key_www)
    file_path = os.path.join(www, path)
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            files = _ls(file_path, show_hidden=False)
            return render_template('index.html',
                                   title='Finder',
                                   files=files)

        else:
            base_name = os.path.basename(file_path)
            # support chinese
            response = send_file(file_path,
                                 as_attachment=True,
                                 attachment_filename=base_name.encode('utf-8'))
            return response
    else:
        abort(404)


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
    else:
        www = os.getcwd()
    app.config[key_www] = www
    app.run(host=ip, port=args.port)
