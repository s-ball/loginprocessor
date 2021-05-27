from http.server import HTTPServer, BaseHTTPRequestHandler
import http.cookies
import secrets
import urllib.parse


class RequestHandler(BaseHTTPRequestHandler):
    page = b'''<html><header><title>Foo</title></header>
            <body><h1>Foo</h1><p>Bar</p></body></html>'''

    def do_GET(self):
        print(self.requestline)
        self.send_response(200)
        sessionid = self.server.get_session_id(self)
        if sessionid is None:
            self.log_message('not connected')
            self.send_header('SESSIONID', '')
            self.end_headers()
            self.wfile.write(b'''<html><header><title>Login page</title></header>
            <body><form id="login" method="POST" action="/auth">
            <input type="text" name="user"/><input type="password" name="password"/>
            <input type="submit" value="Connection"/></form></body></html>''')
        else:
            self.log_message('connected as %s', sessionid)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(self.page)))
            self.end_headers()
            self.wfile.write(self.page)

    def do_POST(self):
        print("login attempt")
        data = self.rfile.read(int(self.headers['Content-Length']))
        params = urllib.parse.parse_qs(data.decode())
        self.send_response(302)
        self.send_header('Location', '/')
        try:
            if params['user'] == ['foo'] and params['password'] == ['bar']:
                self.server.set_session_id(self)
        except LookupError:
            pass
        self.end_headers()


class Server(HTTPServer):
    sessionid = 'SESSIONID'
    sessions = set()

    def get_session_id(self, req):
        cookie_str = req.headers.get('Cookie', '')
        cookie = http.cookies.SimpleCookie(cookie_str)
        try:
            id = cookie['SESSIONID'].value
            if id not in self.sessions:
                id = None
        except (LookupError, AttributeError):
            id = None
        return id

    def set_session_id(self, req, id=None):
        if id is None:
            id = hex(secrets.randbits(64))[2:]
            self.sessions.add(id)
        cookie = http.cookies.SimpleCookie({self.sessionid: id})
        cookie[self.sessionid]['httponly'] = True;
        req.send_header('Set-Cookie', cookie[self.sessionid].OutputString())



if __name__ == '__main__':
    server = Server(('localhost', 8000), RequestHandler)
    server.serve_forever()