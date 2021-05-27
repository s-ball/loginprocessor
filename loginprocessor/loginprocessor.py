import io

from bs4 import BeautifulSoup
from urllib.request import BaseHandler, Request
from urllib.parse import urljoin, urlencode
from http.client import HTTPResponse
import re
import socket
import itertools


class LoginProcessor(BaseHandler):
    field_type = re.compile(r'(text)|(password)', re.IGNORECASE)

    def __init__(self, url: str = None, form_id: str = None, **kwargs):
        self.url = url
        self.form_id = form_id
        if 0 == len(kwargs):
            raise TypeError('At least one form parameter is required')
        self.form_params = kwargs

    def http_response(self, req: Request, resp: HTTPResponse) -> HTTPResponse:
        if resp.getcode() == 200 and (self.url is None
                                      or resp.geturl().startswith(self.url)):
            length = resp.length
            t = resp.read()
            soup = BeautifulSoup(t, features='html.parser')
            attrs = {} if self.form_id is None else {'id': self.form_id}
            for form in soup.find_all('form', **attrs, ):
                fields = form.find_all('input')
                names = [field.attrs.get('name', '') for field in fields
                         if field.attrs.get('type') in ('text', 'password')]
                if not all(k in names for k in self.form_params.keys()):
                    continue
                data = self.form_params.copy()
                for f in fields:
                    if f.attrs.get('type') in ('hidden', 'submit'):
                        try:
                            data[f.attrs['name']] = f.attrs['value']
                        except LookupError:
                            pass
                ans = Request(urljoin(resp.geturl(),
                                      form.attrs.get('action', '.')),
                              method=form.attrs.get('method', 'POST'),
                              data=urlencode(data).encode())
                return self.parent.open(ans, timeout=getattr(
                    req, 'timeout', socket.getdefaulttimeout()))
            resp.fp = io.BytesIO(t)
            resp.length = length
        return resp

    https_response = http_response
