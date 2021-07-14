#encoding: utf-8
import gettext
import binascii
import sys as _sys
import os.path

import six


if _sys.version_info[0] == 2:

    _PY3 = False
    basestring = basestring
    buffer = buffer
    xrange = xrange
    unicode = unicode
    from urllib import quote, unquote
    import httplib
    import xmlrpclib
    from ConfigParser import ConfigParser
    from HTMLParser import HTMLParser
    proj_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    lib_path = proj_path + '/lib'
    _sys.path.append(lib_path)
    from pbkdf2 import pbkdf2_hmac

    def encode_string(s, encoding='latin-1'):
        # do nothing
        return six.b(s)

    def utf8_encode(obj):
        from libcomm import utf8_encode as _utf8_encode
        return _utf8_encode(obj)

    def ensure_string(s, encoding='latin-1'):
        return s

    def simple_ord(c):
        if isinstance(c, str):
            return ord(c)
        return c

    def decode_utf8(s):
        if not isinstance(s, unicode):
            return s.decode('utf-8', 'ignore')

    from hash_ring import HashRing

else:

    _PY3 = True
    buffer = memoryview
    xrange = range
    basestring = str
    from urllib.parse import quote, unquote
    import http.client
    import xmlrpc.client
    httplib = http.client
    xmlrpclib = xmlrpc.client
    from configparser import ConfigParser
    from html.parser import HTMLParser
    from hashlib import pbkdf2_hmac

    def unicode(value, *args):
        # do nothing
        return value

    def encode_string(s, encoding='latin-1'):
        if isinstance(s, str):
            if encoding == 'latin-1':
                return six.b(s) # latin1
            else:
                return s.encode(encoding)
        return s

    def utf8_encode(obj):
        # do nothing
        return obj

    def ensure_string(s, encoding='latin-1'):
        if isinstance(s, str):
            return s
        return s.decode(encoding=encoding)

    def simple_ord(c):
        if isinstance(c, str):
            return ord(c)
        return c

    def decode_utf8(s):
        # do nothing
        return s

    from hashring import HashRing


def is_python3():
    return _PY3


def from_hex(s):
    # type: (str) -> str
    """ Binary data of hexadecimal representation. str -> str
    >>> from_hex('6b4e4743446a1b1c130107') # 'kNGCDj\x1b\x1c\x13\x01\x07'
    'kNGCDj\\x1b\\x1c\\x13\\x01\\x07'
    """
    return ensure_string(binascii.unhexlify(s))

def to_hex(data):
    # type: (bytes) -> str
    """
    >>> to_hex(b'kNGCDj\x1b\x1c\x13\x01\x07')
    '6b4e4743446a1b1c130107'
    """
    return ensure_string(binascii.hexlify(data))

binary_type = six.binary_type


def setup_gettext():
    if is_python3():
        gettext.install('zh_CN')
    else:
        gettext.install('zh_CN', unicode=True)

