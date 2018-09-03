# -*- coding: utf-8 -*-
import cgi
import html
import io
import mimetypes
import os
import posixpath
import shutil
import sys
import time
import urllib
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

from finder import server
import finder.server
from finder.server import daemon

__version__ = '0.1'


class FileHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET and HEAD commands.
    """

    server_version = "SimpleHTTP/" + __version__

    base_dir = os.getcwd()
    support_upload = False

    def do_POST(self):
        try:
            formdata = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         }
            )
            save_path = formdata['path'].value
            self.path = save_path
            """:type:str"""
            if save_path.startswith('/'):
                save_path = save_path[1:]
            save_file = formdata['file']
            file_name = save_file.filename
            file_value = save_file.value
            if file_name:
                file_path = os.path.join(self.base_dir, save_path, file_name)
                if not os.path.exists(file_path):
                    f = open(file_path, 'bw')
                    f.write(file_value)
                    f.close()
                    print('file[%s] upload success' % file_name)
                else:
                    print('file[%s] exit' % file_name)
        except KeyError:
            pass
        # print result
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            parts = urllib.parse.urlsplit(self.path)
            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                new_parts = (parts[0], parts[1], parts[2] + '/',
                             parts[3], parts[4])
                new_url = urllib.parse.urlunsplit(new_parts)
                self.send_header("Location", new_url)
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        try:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).
        """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        ######
        r = []
        if displaypath != '/':
            r.append(server.table_tr(file_href='../', file_title='<-back', file_time='-'))
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            href = urllib.parse.quote(linkname,
                                      errors='surrogatepass')
            title = html.escape(displayname, quote=False)
            file_stat = os.stat(fullname)
            modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(file_stat.st_mtime))
            if os.path.isdir(fullname):
                size = '-'
            else:
                size = server.convert_file_size(file_stat.st_size)
            r.append(server.table_tr(file_href=href, file_title=title, file_time=modify_time, file_size=size))
        table_tbody = '\n'.join(r)
        encoded = server.index_content(request_path=displaypath, table_content=table_tbody,
                                       support_upload=self.support_upload)
        ######
        encoded = encoded.encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        ######
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = self.base_dir
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                # Ignore components that are not a simple file/directory name
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.
        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.
        Argument is a PATH (a filename).
        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def run_server(port=8000, bind="", base_dir=os.getcwd(), show_qr=False, support_upload=False, daemon_start=False,
               pid_file='/var/run/finder.pid', log_file='/var/log/finder.log'):
    """Test the HTTP request handler class.

    This runs an HTTP server on port 8000 (or the port argument).

    """
    protocol = "HTTP/1.0"
    server_address = (bind, port)
    FileHTTPRequestHandler.base_dir = base_dir
    FileHTTPRequestHandler.protocol_version = protocol
    FileHTTPRequestHandler.support_upload = support_upload
    with HTTPServer(server_address, FileHTTPRequestHandler) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            if show_qr:
                server.qr_code_show('http://{host}:{port}/'.format(host=sa[0], port=sa[1]))
            if daemon_start:
                daemon.daemon_exec(command='start', pid_file=pid_file, log_file=log_file)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    run_server(base_dir='/Users/hyxf', support_upload=True)
