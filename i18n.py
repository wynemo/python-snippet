# -*- coding: utf-8 -*-
import gettext
from functools import partial

from lib6 import _PY3
from util.lazystring import _LazyString

zh_lang = None
en_lang = None
zh_hk_lang = None

LOCALE_DIR = ''


def get_language_obj(language):
    global zh_lang
    global en_lang
    global zh_hk_lang
    if language == 'en':
        if not en_lang:
            en_lang = gettext.translation('en_US', LOCALE_DIR, languages=['en_US'])
        return en_lang
    elif language == 'zh_HK':
        if not zh_hk_lang:
            zh_hk_lang = gettext.translation('zh_HK', LOCALE_DIR, languages=['zh_HK'])
        return zh_hk_lang
    else:
        if not zh_lang:
            zh_lang = gettext.translation('zh_CN', LOCALE_DIR, languages=['zh_CN'])
        return zh_lang


def setup_translation(language):
    if _PY3:
        import builtins
        builtins.__dict__['_'] = partial(lazy_translate, language=language)
    else:
        import __builtin__
        __builtin__.__dict__['_'] = partial(lazy_translate, language=language)


def translate(message, language=None):
    msg = message
    while isinstance(msg, _LazyString):
        msg = message._args[0]
    if _PY3:
        return get_language_obj(language).gettext(msg)
    else:
        return get_language_obj(language).ugettext(msg)


def lazy_translate(message, language=None):
    obj = _LazyString(translate, message, language=language)
    return obj


if __name__ == '__main__':
    import partial
    setup_translation('en')
    s = _('帐号或密码错误')
    # print(s)
    c_s = lazy_translate(s, 'zh_CN')
    assert c_s == '帐号或密码错误'
    assert s == 'Invalid username or password'
    s = _('test %s')
    x = s % '123'
    print(x)

    class A(object):
        pass

    def test_func():
        a = A()
        print(a.xxx)

    try:
        obj = _LazyString(test_func)
        print(obj)
    except Exception as e:
        print(e)

    _ = partial(translate, language='en')
    _('测试')
    
