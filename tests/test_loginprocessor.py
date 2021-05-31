import http.client
import io
import unittest
import urllib.request

from loginprocessor.loginprocessor import LoginProcessor
from unittest.mock import Mock
import email.parser


class TestLoginProcessor(unittest.TestCase):
    def test_init_no_params(self):
        with self.assertRaises(TypeError):
            LoginProcessor()

    def test_bad_form_id(self):
        lp = LoginProcessor('/foo', 'bar', key='x')
        b = b'''<HTML><BODY><FORM id="baz"><INPUT name="key" type="text"/></form></HTML>'''
        resp = Mock(http.client.HTTPResponse, wraps=io.BytesIO(b),
                    getcode=Mock(return_value=200),
                    geturl=Mock(return_value='/foo'),
                    length=len(b),
                    headers = email.parser.Parser(_class=http.client.HTTPMessage).parsestr(''))
        r = lp.http_response(urllib.request.Request('http://foo.org/foo'), resp)
        self.assertIs(resp, r)

    def test_bad_param(self):
        lp = LoginProcessor('/foo', 'bar', key='x')
        b = b'''<HTML><BODY><FORM id="bar"><INPUT name="key_x" type="text"/></form></HTML>'''
        resp = Mock(http.client.HTTPResponse, wraps=io.BytesIO(b),
                    getcode=Mock(return_value=200),
                    geturl=Mock(return_value='/foo'),
                    length=len(b),
                    headers = email.parser.Parser(_class=http.client.HTTPMessage).parsestr(''))
        r = lp.http_response(urllib.request.Request('http://foo.org/foo'), resp)
        self.assertIs(resp, r)

    def test_redir(self):
        lp = LoginProcessor('http://foo.org', 'bar', key='x')
        resp2 = Mock(http.client.HTTPResponse)
        parent = Mock(urllib.request.OpenerDirector, **{'open.return_value': resp2})
        lp.add_parent(parent)
        b = b'''<HTML><BODY><FORM id="bar"><INPUT name="key" type="text"/></form></HTML>'''
        resp = Mock(http.client.HTTPResponse, wraps=io.BytesIO(b),
                    getcode=Mock(return_value=200),
                    geturl=Mock(return_value='http://foo.org/fee'),
                    length=len(b))
        r = lp.http_response(urllib.request.Request('http://foo.org/foo'), resp)
        self.assertIs(resp2, r)

    def test_read(self):
        lp = LoginProcessor('/foo', 'bar', key='x')
        b = b'''<HTML><BODY><FORM id="bar"><INPUT name="key_x" type="text"/></form></HTML>'''
        resp = Mock(http.client.HTTPResponse, wraps=io.BytesIO(b),
                    getcode=Mock(return_value=200),
                    geturl=Mock(return_value='/foo'),
                    length=len(b),
                    headers = email.parser.Parser(_class=http.client.HTTPMessage).parsestr(''))
        r = lp.http_response(urllib.request.Request('http://foo.org/foo'), resp)
        self.assertIs(resp, r)
        self.assertEqual(b, r.fp.read())


if __name__ == '__main__':
    unittest.main()
