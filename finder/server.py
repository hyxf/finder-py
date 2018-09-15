# -*- coding: utf-8 -*-
import os
from functools import wraps

from flask import Flask, abort, send_file, request, Response
from flask import render_template

from finder import daemon
from finder import utils

app = Flask(__name__, static_folder='static', template_folder='templates')

key_www = 'www'
key_upload = 'upload'
key_user = 'user'
key_pass = 'pass'


def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = app.config.get(key_user)
        passwd = app.config.get(key_pass)
        if user and passwd:
            auth = request.authorization
            if not auth or not (user == auth.username and passwd == auth.password):
                return _not_authenticated()
        return f(*args, **kwargs)

    return decorated


def _not_authenticated():
    """Sends a 401 response that enables basic auth
    """
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def _ls(path, show_hidden=True):
    www = app.config.get(key_www)
    lists = os.listdir(path)
    if not show_hidden:
        lists = [x for x in lists if not x.startswith('.')]
    files = []
    for file_name in lists:
        file_path = os.path.join(path, file_name)
        file_map = {'path': file_path.replace(www, ''),
                    'isfile': os.path.isfile(file_path),
                    'name': file_name,
                    'time': utils.get_file_time(file_path),
                    'size': utils.get_file_size(file_path) if os.path.isfile(file_path) else '-'}
        files.append(file_map)
    return files


@app.route('/mkdir', methods=['POST'])
def mkdir():
    """
    file delete
    :return:
    """
    www = app.config.get(key_www)
    path = request.form['path']
    name = request.form['name']
    path = path[1:] if path.startswith('/') else path
    file_path = os.path.join(www, path, name)
    try:
        os.mkdir(file_path)
        return "1"
    except Exception:
        return "0"


@app.route('/delete', methods=['POST'])
def delete():
    """
    file delete
    :return:
    """
    www = app.config.get(key_www)
    path = request.form['path']
    path = path[1:] if path.startswith('/') else path
    file_path = os.path.join(www, path)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return "1"
        except Exception:
            return "0"
    else:
        return "0"


@app.route('/upload', methods=['POST'])
def upload():
    """
    file upload
    :return:
    """
    www = app.config.get(key_www)
    path = request.form['path']
    ufile = request.files['file']
    """:type :werkzeug.datastructures.FileStorage"""
    file_path = os.path.join(www, path[1:], ufile.filename)
    ufile.save(dst=file_path)
    return 'success'


@app.route('/', defaults={'path': '/'}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@basic_auth_required
def index_path(path):
    """
    index for path
    :param path:
    :return:
    """
    www = app.config.get(key_www)
    is_root = path == '/'
    file_path = www if is_root else os.path.join(www, path)
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            files = _ls(file_path, show_hidden=False)
            return render_template('index.html',
                                   title='Finder',
                                   files=files,
                                   nav=False if is_root else True,
                                   path=path if path.startswith('/') else '/{0}'.format(path),
                                   upload=app.config.get(key_upload))

        else:
            base_name = os.path.basename(file_path)
            # support chinese
            response = send_file(file_path,
                                 as_attachment=True,
                                 attachment_filename=base_name.encode('utf-8'))
            return response
    else:
        abort(404)


@app.route('/up88/', defaults={'path': '/'}, methods=['GET'])
@app.route('/up88/<path:path>', methods=['GET'])
@basic_auth_required
def upload_path(path):
    """
    upload for path
    :param path:
    :return:
    """
    www = app.config.get(key_www)
    return render_template('upload.html',
                           title='Finder',
                           files=[],
                           nav=True,
                           path=path if path.startswith('/') else '/{0}'.format(path),
                           upload=app.config.get(key_upload))


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
    app.config[key_upload] = args.upload
    app.config[key_user] = args.user
    app.config[key_pass] = args.password
    if args.qr:
        utils.qr_code_show('http://{0}:{1}/'.format(ip, args.port))
    if args.start:
        daemon.daemon_exec(command='start',
                           pid_file=args.pid_file,
                           log_file=args.log_file)
    app.run(host=ip, port=args.port)
