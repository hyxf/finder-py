# -*- coding: utf-8 -*-
import os

from flask import Flask, abort, send_from_directory, make_response
from flask import render_template

from finder import daemon
from finder import utils

app = Flask(__name__, static_folder='static', template_folder='templates')

key_www = 'www'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
                           title='qiudongchao')


@app.route('/<path:path>', methods=['GET'])
def index_path(path):
    www = app.config.get(key_www)
    file_path = os.path.join(www, path)
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            pass
        else:
            base_name = os.path.basename(file_path)
            base_dir = os.path.dirname(file_path)
            response = make_response(send_from_directory(base_dir, base_name, as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                base_name.encode('ascii').decode('utf-8'))
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
