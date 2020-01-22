import unittest

from sixectomy import compatibility
from sixectomy import exceptions

lines = [
    'MovedAttribute("cStringIO", "cStringIO", "io", "StringIO"),\n',
    'MovedAttribute("filter", "itertools", "builtins", "ifilter", "filter"),\n',
    'MovedAttribute("filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse"),\n',  # noqa
    'MovedAttribute("input", "__builtin__", "builtins", "raw_input", "input"),\n',  # noqa
    'MovedAttribute("intern", "__builtin__", "sys"),\n',
    'MovedAttribute("map", "itertools", "builtins", "imap", "map"),\n',
    'MovedAttribute("getcwd", "os", "os", "getcwdu", "getcwd"),\n',
    'MovedAttribute("getcwdb", "os", "os", "getcwd", "getcwdb"),\n',
    'MovedAttribute("getoutput", "commands", "subprocess"),\n',
    'MovedAttribute("range", "__builtin__", "builtins", "xrange", "range"),\n',
    'MovedAttribute("reload_module", "__builtin__", "importlib" if PY34 else "imp", "reload"),\n',  # noqa
    'MovedAttribute("reduce", "__builtin__", "functools"),\n',
    'MovedAttribute("shlex_quote", "pipes", "shlex", "quote"),\n',
    'MovedAttribute("StringIO", "StringIO", "io"),\n',
    'MovedAttribute("UserDict", "UserDict", "collections"),\n',
    'MovedAttribute("UserList", "UserList", "collections"),\n',
    'MovedAttribute("UserString", "UserString", "collections"),\n',
    'MovedAttribute("xrange", "__builtin__", "builtins", "xrange", "range"),\n',  # noqa
    'MovedAttribute("zip", "itertools", "builtins", "izip", "zip"),\n',
    'MovedAttribute("zip_longest", "itertools", "itertools", "izip_longest", "zip_longest"),\n',  # noqa
    'MovedModule("builtins", "__builtin__"),\n',
    'MovedModule("configparser", "ConfigParser"),\n',
    'MovedModule("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections"),\n',  # noqa
    'MovedModule("copyreg", "copy_reg"),\n',
    'MovedModule("dbm_gnu", "gdbm", "dbm.gnu"),\n',
    'MovedModule("dbm_ndbm", "dbm", "dbm.ndbm"),\n',
    'MovedModule("_dummy_thread", "dummy_thread", "_dummy_thread" if sys.version_info < (3, 9) else "_thread"),\n',  # noqa
    'MovedModule("http_cookiejar", "cookielib", "http.cookiejar"),\n',
    'MovedModule("http_cookies", "Cookie", "http.cookies"),\n',
    'MovedModule("html_entities", "htmlentitydefs", "html.entities"),\n',
    'MovedModule("html_parser", "HTMLParser", "html.parser"),\n',
    'MovedModule("http_client", "httplib", "http.client"),\n',
    'MovedModule("email_mime_base", "email.MIMEBase", "email.mime.base"),\n',
    'MovedModule("email_mime_image", "email.MIMEImage", "email.mime.image"),\n',  # noqa
    'MovedModule("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart"),\n',  # noqa
    'MovedModule("email_mime_nonmultipart", "email.MIMENonMultipart", "email.mime.nonmultipart"),\n',  # noqa
    'MovedModule("email_mime_text", "email.MIMEText", "email.mime.text"),\n',
    'MovedModule("BaseHTTPServer", "BaseHTTPServer", "http.server"),\n',
    'MovedModule("CGIHTTPServer", "CGIHTTPServer", "http.server"),\n',
    'MovedModule("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),\n',
    'MovedModule("cPickle", "cPickle", "pickle"),\n',
    'MovedModule("queue", "Queue"),\n',
    'MovedModule("reprlib", "repr"),\n',
    'MovedModule("socketserver", "SocketServer"),\n',
    'MovedModule("_thread", "thread", "_thread"),\n',
    'MovedModule("tkinter", "Tkinter"),\n',
    'MovedModule("tkinter_dialog", "Dialog", "tkinter.dialog"),\n',
    'MovedModule("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),\n',
    'MovedModule("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),\n',  # noqa
    'MovedModule("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),\n',  # noqa
    'MovedModule("tkinter_tix", "Tix", "tkinter.tix"),\n',
    'MovedModule("tkinter_ttk", "ttk", "tkinter.ttk"),\n',
    'MovedModule("tkinter_constants", "Tkconstants", "tkinter.constants"),\n',
    'MovedModule("tkinter_dnd", "Tkdnd", "tkinter.dnd"),\n',
    'MovedModule("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser"),\n',  # noqa
    'MovedModule("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog"),\n',  # noqa
    'MovedModule("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),\n',  # noqa
    'MovedModule("tkinter_font", "tkFont", "tkinter.font"),\n',
    'MovedModule("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),\n',  # noqa
    'MovedModule("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog"),\n',  # noqa
    'MovedModule("urllib_parse", __name__ + ".moves.urllib_parse", "urllib.parse"),\n',  # noqa
    'MovedModule("urllib_error", __name__ + ".moves.urllib_error", "urllib.error"),\n',  # noqa
    'MovedModule("urllib", __name__ + ".moves.urllib", __name__ + ".moves.urllib"),\n',  # noqa
    'MovedModule("urllib_robotparser", "robotparser", "urllib.robotparser"),\n',  # noqa
    'MovedModule("xmlrpc_client", "xmlrpclib", "xmlrpc.client"),\n',
    'MovedModule("xmlrpc_server", "SimpleXMLRPCServer", "xmlrpc.server"),\n',
    'MovedModule("winreg", "_winreg"),\n',
    'MovedAttribute("ParseResult", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("SplitResult", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("parse_qs", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("parse_qsl", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urldefrag", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urljoin", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urlparse", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urlsplit", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urlunparse", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("urlunsplit", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("quote", "urllib", "urllib.parse"),\n',
    'MovedAttribute("quote_plus", "urllib", "urllib.parse"),\n',
    'MovedAttribute("unquote", "urllib", "urllib.parse"),\n',
    'MovedAttribute("unquote_plus", "urllib", "urllib.parse"),\n',
    'MovedAttribute("unquote_to_bytes", "urllib", "urllib.parse", "unquote", "unquote_to_bytes"),\n',  # noqa
    'MovedAttribute("urlencode", "urllib", "urllib.parse"),\n',
    'MovedAttribute("splitquery", "urllib", "urllib.parse"),\n',
    'MovedAttribute("splittag", "urllib", "urllib.parse"),\n',
    'MovedAttribute("splituser", "urllib", "urllib.parse"),\n',
    'MovedAttribute("splitvalue", "urllib", "urllib.parse"),\n',
    'MovedAttribute("uses_fragment", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("uses_netloc", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("uses_params", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("uses_query", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("uses_relative", "urlparse", "urllib.parse"),\n',
    'MovedAttribute("URLError", "urllib2", "urllib.error"),\n',
    'MovedAttribute("HTTPError", "urllib2", "urllib.error"),\n',
    'MovedAttribute("ContentTooShortError", "urllib", "urllib.error"),\n',
    'MovedAttribute("urlopen", "urllib2", "urllib.request"),\n',
    'MovedAttribute("install_opener", "urllib2", "urllib.request"),\n',
    'MovedAttribute("build_opener", "urllib2", "urllib.request"),\n',
    'MovedAttribute("pathname2url", "urllib", "urllib.request"),\n',
    'MovedAttribute("url2pathname", "urllib", "urllib.request"),\n',
    'MovedAttribute("getproxies", "urllib", "urllib.request"),\n',
    'MovedAttribute("Request", "urllib2", "urllib.request"),\n',
    'MovedAttribute("OpenerDirector", "urllib2", "urllib.request"),\n',
    'MovedAttribute("HTTPDefaultErrorHandler", "urllib2", "urllib.request"),\n',  # noqa
    'MovedAttribute("HTTPRedirectHandler", "urllib2", "urllib.request"),\n',
    'MovedAttribute("HTTPCookieProcessor", "urllib2", "urllib.request"),\n',
    'MovedAttribute("ProxyHandler", "urllib2", "urllib.request"),\n',
    'MovedAttribute("BaseHandler", "urllib2", "urllib.request"),\n',
    'MovedAttribute("HTTPPasswordMgr", "urllib2", "urllib.request"),\n',
    'MovedAttribute("HTTPPasswordMgrWithDefaultRealm", "urllib2", "urllib.request"),\n',  # noqa
    'MovedAttribute("AbstractBasicAuthHandler", "urllib2", "urllib.request"),\n',  # noqa
    'MovedAttribute("HTTPBasicAuthHandler", "urllib2", "urllib.request"),\n',
]

expected_types = [
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedModule',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
    'MovedAttribute',
]

expected_extract = [
    '("cStringIO", "cStringIO", "io", "StringIO")',
    '("filter", "itertools", "builtins", "ifilter", "filter")',
    '("filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse")',
    '("input", "__builtin__", "builtins", "raw_input", "input")',
    '("intern", "__builtin__", "sys")',
    '("map", "itertools", "builtins", "imap", "map")',
    '("getcwd", "os", "os", "getcwdu", "getcwd")',
    '("getcwdb", "os", "os", "getcwd", "getcwdb")',
    '("getoutput", "commands", "subprocess")',
    '("range", "__builtin__", "builtins", "xrange", "range")',
    '("reload_module", "__builtin__", "importlib" if PY34 else "imp", "reload")',  # noqa
    '("reduce", "__builtin__", "functools")',
    '("shlex_quote", "pipes", "shlex", "quote")',
    '("StringIO", "StringIO", "io")',
    '("UserDict", "UserDict", "collections")',
    '("UserList", "UserList", "collections")',
    '("UserString", "UserString", "collections")',
    '("xrange", "__builtin__", "builtins", "xrange", "range")',
    '("zip", "itertools", "builtins", "izip", "zip")',
    '("zip_longest", "itertools", "itertools", "izip_longest", "zip_longest")',
    '("builtins", "__builtin__")',
    '("configparser", "ConfigParser")',
    '("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections")',  # noqa
    '("copyreg", "copy_reg")',
    '("dbm_gnu", "gdbm", "dbm.gnu")',
    '("dbm_ndbm", "dbm", "dbm.ndbm")',
    '("_dummy_thread", "dummy_thread", "_dummy_thread" if sys.version_info < (3, 9) else "_thread")',  # noqa
    '("http_cookiejar", "cookielib", "http.cookiejar")',
    '("http_cookies", "Cookie", "http.cookies")',
    '("html_entities", "htmlentitydefs", "html.entities")',
    '("html_parser", "HTMLParser", "html.parser")',
    '("http_client", "httplib", "http.client")',
    '("email_mime_base", "email.MIMEBase", "email.mime.base")',
    '("email_mime_image", "email.MIMEImage", "email.mime.image")',
    '("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart")',
    '("email_mime_nonmultipart", "email.MIMENonMultipart", "email.mime.nonmultipart")',  # noqa
    '("email_mime_text", "email.MIMEText", "email.mime.text")',
    '("BaseHTTPServer", "BaseHTTPServer", "http.server")',
    '("CGIHTTPServer", "CGIHTTPServer", "http.server")',
    '("SimpleHTTPServer", "SimpleHTTPServer", "http.server")',
    '("cPickle", "cPickle", "pickle")',
    '("queue", "Queue")',
    '("reprlib", "repr")',
    '("socketserver", "SocketServer")',
    '("_thread", "thread", "_thread")',
    '("tkinter", "Tkinter")',
    '("tkinter_dialog", "Dialog", "tkinter.dialog")',
    '("tkinter_filedialog", "FileDialog", "tkinter.filedialog")',
    '("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext")',
    '("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog")',
    '("tkinter_tix", "Tix", "tkinter.tix")',
    '("tkinter_ttk", "ttk", "tkinter.ttk")',
    '("tkinter_constants", "Tkconstants", "tkinter.constants")',
    '("tkinter_dnd", "Tkdnd", "tkinter.dnd")',
    '("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser")',
    '("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog")',
    '("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog")',
    '("tkinter_font", "tkFont", "tkinter.font")',
    '("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox")',
    '("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog")',
    '("urllib_parse", __name__ + ".moves.urllib_parse", "urllib.parse")',  # noqa
    '("urllib_error", __name__ + ".moves.urllib_error", "urllib.error")',  # noqa
    '("urllib", __name__ + ".moves.urllib", __name__ + ".moves.urllib")',  # noqa
    '("urllib_robotparser", "robotparser", "urllib.robotparser")',
    '("xmlrpc_client", "xmlrpclib", "xmlrpc.client")',
    '("xmlrpc_server", "SimpleXMLRPCServer", "xmlrpc.server")',
    '("winreg", "_winreg")',
    '("ParseResult", "urlparse", "urllib.parse")',
    '("SplitResult", "urlparse", "urllib.parse")',
    '("parse_qs", "urlparse", "urllib.parse")',
    '("parse_qsl", "urlparse", "urllib.parse")',
    '("urldefrag", "urlparse", "urllib.parse")',
    '("urljoin", "urlparse", "urllib.parse")',
    '("urlparse", "urlparse", "urllib.parse")',
    '("urlsplit", "urlparse", "urllib.parse")',
    '("urlunparse", "urlparse", "urllib.parse")',
    '("urlunsplit", "urlparse", "urllib.parse")',
    '("quote", "urllib", "urllib.parse")',
    '("quote_plus", "urllib", "urllib.parse")',
    '("unquote", "urllib", "urllib.parse")',
    '("unquote_plus", "urllib", "urllib.parse")',
    '("unquote_to_bytes", "urllib", "urllib.parse", "unquote", "unquote_to_bytes")',  # noqa
    '("urlencode", "urllib", "urllib.parse")',
    '("splitquery", "urllib", "urllib.parse")',
    '("splittag", "urllib", "urllib.parse")',
    '("splituser", "urllib", "urllib.parse")',
    '("splitvalue", "urllib", "urllib.parse")',
    '("uses_fragment", "urlparse", "urllib.parse")',
    '("uses_netloc", "urlparse", "urllib.parse")',
    '("uses_params", "urlparse", "urllib.parse")',
    '("uses_query", "urlparse", "urllib.parse")',
    '("uses_relative", "urlparse", "urllib.parse")',
    '("URLError", "urllib2", "urllib.error")',
    '("HTTPError", "urllib2", "urllib.error")',
    '("ContentTooShortError", "urllib", "urllib.error")',
    '("urlopen", "urllib2", "urllib.request")',
    '("install_opener", "urllib2", "urllib.request")',
    '("build_opener", "urllib2", "urllib.request")',
    '("pathname2url", "urllib", "urllib.request")',
    '("url2pathname", "urllib", "urllib.request")',
    '("getproxies", "urllib", "urllib.request")',
    '("Request", "urllib2", "urllib.request")',
    '("OpenerDirector", "urllib2", "urllib.request")',
    '("HTTPDefaultErrorHandler", "urllib2", "urllib.request")',
    '("HTTPRedirectHandler", "urllib2", "urllib.request")',
    '("HTTPCookieProcessor", "urllib2", "urllib.request")',
    '("ProxyHandler", "urllib2", "urllib.request")',
    '("BaseHandler", "urllib2", "urllib.request")',
    '("HTTPPasswordMgr", "urllib2", "urllib.request")',
    '("HTTPPasswordMgrWithDefaultRealm", "urllib2", "urllib.request")',
    '("AbstractBasicAuthHandler", "urllib2", "urllib.request")',
    '("HTTPBasicAuthHandler", "urllib2", "urllib.request")',
]

expected_evals = [
    ("cStringIO", "cStringIO", "io", "StringIO"),
    ("filter", "itertools", "builtins", "ifilter", "filter"),
    ("filterfalse", "itertools", "itertools", "ifilterfalse", "filterfalse"),
    ("input", "__builtin__", "builtins", "raw_input", "input"),
    ("intern", "__builtin__", "sys"),
    ("map", "itertools", "builtins", "imap", "map"),
    ("getcwd", "os", "os", "getcwdu", "getcwd"),
    ("getcwdb", "os", "os", "getcwd", "getcwdb"),
    ("getoutput", "commands", "subprocess"),
    ("range", "__builtin__", "builtins", "xrange", "range"),
    ("reload_module", "__builtin__", "importlib", "reload"),
    ("reduce", "__builtin__", "functools"),
    ("shlex_quote", "pipes", "shlex", "quote"),
    ("StringIO", "StringIO", "io"),
    ("UserDict", "UserDict", "collections"),
    ("UserList", "UserList", "collections"),
    ("UserString", "UserString", "collections"),
    ("xrange", "__builtin__", "builtins", "xrange", "range"),
    ("zip", "itertools", "builtins", "izip", "zip"),
    ("zip_longest", "itertools", "itertools", "izip_longest", "zip_longest"),
    ("builtins", "__builtin__"),
    ("configparser", "ConfigParser"),
    ("collections_abc", "collections", "collections.abc"),
    ("copyreg", "copy_reg"),
    ("dbm_gnu", "gdbm", "dbm.gnu"),
    ("dbm_ndbm", "dbm", "dbm.ndbm"),
    ("_dummy_thread", "dummy_thread", "_dummy_thread"),
    ("http_cookiejar", "cookielib", "http.cookiejar"),
    ("http_cookies", "Cookie", "http.cookies"),
    ("html_entities", "htmlentitydefs", "html.entities"),
    ("html_parser", "HTMLParser", "html.parser"),
    ("http_client", "httplib", "http.client"),
    ("email_mime_base", "email.MIMEBase", "email.mime.base"),
    ("email_mime_image", "email.MIMEImage", "email.mime.image"),
    ("email_mime_multipart", "email.MIMEMultipart", "email.mime.multipart"),
    ("email_mime_nonmultipart", "email.MIMENonMultipart", "email.mime.nonmultipart"),  # noqa
    ("email_mime_text", "email.MIMEText", "email.mime.text"),
    ("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    ("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    ("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    ("cPickle", "cPickle", "pickle"),
    ("queue", "Queue"),
    ("reprlib", "repr"),
    ("socketserver", "SocketServer"),
    ("_thread", "thread", "_thread"),
    ("tkinter", "Tkinter"),
    ("tkinter_dialog", "Dialog", "tkinter.dialog"),
    ("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    ("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    ("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    ("tkinter_tix", "Tix", "tkinter.tix"),
    ("tkinter_ttk", "ttk", "tkinter.ttk"),
    ("tkinter_constants", "Tkconstants", "tkinter.constants"),
    ("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    ("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser"),
    ("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog"),
    ("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    ("tkinter_font", "tkFont", "tkinter.font"),
    ("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    ("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog"),
    ("urllib_parse", "six.moves.urllib_parse", "urllib.parse"),
    ("urllib_error", "six.moves.urllib_error", "urllib.error"),
    ("urllib", "six.moves.urllib", "six.moves.urllib"),
    ("urllib_robotparser", "robotparser", "urllib.robotparser"),
    ("xmlrpc_client", "xmlrpclib", "xmlrpc.client"),
    ("xmlrpc_server", "SimpleXMLRPCServer", "xmlrpc.server"),
    ("winreg", "_winreg"),
    ("ParseResult", "urlparse", "urllib.parse"),
    ("SplitResult", "urlparse", "urllib.parse"),
    ("parse_qs", "urlparse", "urllib.parse"),
    ("parse_qsl", "urlparse", "urllib.parse"),
    ("urldefrag", "urlparse", "urllib.parse"),
    ("urljoin", "urlparse", "urllib.parse"),
    ("urlparse", "urlparse", "urllib.parse"),
    ("urlsplit", "urlparse", "urllib.parse"),
    ("urlunparse", "urlparse", "urllib.parse"),
    ("urlunsplit", "urlparse", "urllib.parse"),
    ("quote", "urllib", "urllib.parse"),
    ("quote_plus", "urllib", "urllib.parse"),
    ("unquote", "urllib", "urllib.parse"),
    ("unquote_plus", "urllib", "urllib.parse"),
    ("unquote_to_bytes", "urllib", "urllib.parse", "unquote", "unquote_to_bytes"),  # noqa
    ("urlencode", "urllib", "urllib.parse"),
    ("splitquery", "urllib", "urllib.parse"),
    ("splittag", "urllib", "urllib.parse"),
    ("splituser", "urllib", "urllib.parse"),
    ("splitvalue", "urllib", "urllib.parse"),
    ("uses_fragment", "urlparse", "urllib.parse"),
    ("uses_netloc", "urlparse", "urllib.parse"),
    ("uses_params", "urlparse", "urllib.parse"),
    ("uses_query", "urlparse", "urllib.parse"),
    ("uses_relative", "urlparse", "urllib.parse"),
    ("URLError", "urllib2", "urllib.error"),
    ("HTTPError", "urllib2", "urllib.error"),
    ("ContentTooShortError", "urllib", "urllib.error"),
    ("urlopen", "urllib2", "urllib.request"),
    ("install_opener", "urllib2", "urllib.request"),
    ("build_opener", "urllib2", "urllib.request"),
    ("pathname2url", "urllib", "urllib.request"),
    ("url2pathname", "urllib", "urllib.request"),
    ("getproxies", "urllib", "urllib.request"),
    ("Request", "urllib2", "urllib.request"),
    ("OpenerDirector", "urllib2", "urllib.request"),
    ("HTTPDefaultErrorHandler", "urllib2", "urllib.request"),
    ("HTTPRedirectHandler", "urllib2", "urllib.request"),
    ("HTTPCookieProcessor", "urllib2", "urllib.request"),
    ("ProxyHandler", "urllib2", "urllib.request"),
    ("BaseHandler", "urllib2", "urllib.request"),
    ("HTTPPasswordMgr", "urllib2", "urllib.request"),
    ("HTTPPasswordMgrWithDefaultRealm", "urllib2", "urllib.request"),
    ("AbstractBasicAuthHandler", "urllib2", "urllib.request"),
    ("HTTPBasicAuthHandler", "urllib2", "urllib.request"),
]


class TestCompatibility(unittest.TestCase):
    def setUp(self):
        self.compat = compatibility.Compatibility()

    def test_init(self):
        expected = ("")
        self.assertTrue(isinstance(self.compat, list))

    def test_parse_line(self):
        # Testing specific use cases just to be sure everything is ok
        # before looping automatically over lot of test cases. also help
        # to be focused on specific use cases and to develop the feature.
        given = 'MovedAttribute("cStringIO", "cStringIO", "io", "StringIO"),\n'
        expected_typeof = 'MovedAttribute'
        expected_value = '("cStringIO", "cStringIO", "io", "StringIO")'
        typeof, value = compatibility.parse_line(given)
        self.assertEqual(typeof, expected_typeof)
        self.assertEqual(value, expected_value)

        with self.assertRaises(exceptions.SixectomyCompatibilityException):
            compatibility.parse_line("boom")

        given = 'MovedAttribute("filter", "itertools", "builtins", "ifilter", "filter"),\n'  # noqa
        expected_typeof = 'MovedAttribute'
        expected_value = '("filter", "itertools", "builtins", "ifilter", "filter")'
        typeof, value = compatibility.parse_line(given)
        self.assertEqual(typeof, expected_typeof)
        self.assertEqual(value, expected_value)

        given = 'MovedModule("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections"),\n'  # noqa
        expected_typeof = 'MovedModule'
        expected_value = '("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections")'  # noqa
        typeof, value = compatibility.parse_line(given)
        self.assertEqual(typeof, expected_typeof)
        self.assertEqual(value, expected_value)

        # Testing all tests cases to ensure every use cases works fine.
        for index, line in enumerate(lines):
            typeof, value = compatibility.parse_line(line)
            self.assertEqual(typeof, expected_types[index])
            self.assertEqual(value, expected_extract[index])

    def test_eval_line(self):
        # Testing specific use cases just to be sure everything is ok
        # before looping automatically over lot of test cases. also help
        # to be focused on specific use cases and to develop the feature.
        given = '("collections_abc", "collections", "collections.abc" if sys.version_info >= (3, 3) else "collections")'  # noqa
        expected = ("collections_abc", "collections", "collections.abc")
        self.assertEqual(compatibility.eval_line(given), expected)

        # Testing all tests cases to ensure every use cases works fine.
        for index, line in enumerate(expected_extract):
            self.assertEqual(
                compatibility.eval_line(line),
                expected_evals[index]
            )

    def test_read_six_sources(self):
        for line in self.compat._sources:
            self.assertTrue((
                line.startswith('MovedModule(') or \
                line.startswith('MovedAttribute(')
            ))
            # Check if call on MovedModule or MovedAttribute with multiple
            # lines are well merged (line and line + 1)
            # Example => https://github.com/benjaminp/six/blob/3a3db7510b33eb22c63ad94bc735a9032949249f/six.py#L290,L291  # noqa
            self.assertTrue((
                line[-2:] == '),' or \
                line[-2:] == ')'
            ))

    def test_setup_binding(self):
        for index, line in enumerate(expected_evals):
            self.assertTrue(line[0] in self.compat._mapping)
            self.assertEqual(
                self.compat._mapping[line[0]]["type"],
                expected_types[index])
            self.assertEqual(self.compat._mapping[line[0]]["value"], line)

    def test_lookup(self):
        expected = {
            "type": "MovedModule",
            "value": ("collections_abc", "collections", "collections.abc")
        }
        self.assertEqual(self.compat.lookup("collections_abc"), expected)
        expected = {
            "type": "MovedModule",
            "value": ("collections_abc", "collections", "collections.abc")
        }
        self.assertEqual(self.compat.lookup("six.collections_abc"), expected)
        expected = {
            "type": "MovedModule",
            "value": ("collections_abc", "collections", "collections.abc")
        }
        self.assertEqual(
            self.compat.lookup("six.moves.collections_abc"),
            expected
        )
        with self.assertRaises(exceptions.SixectomyCompatibilityNotFound):
            self.compat.lookup("six.moves.collectio_abc")
        expected = {
            "type": "MovedModule",
            "value": ("urllib_parse", "six.moves.urllib_parse", "urllib.parse")
        }
        self.assertEqual(
            self.compat.lookup("six.moves.urllib.parse"),
            expected
        )
        expected = {
            "type": "MovedModule",
            "value": ("urllib_parse", "six.moves.urllib_parse", "urllib.parse")
        }
        self.assertEqual(
            self.compat.lookup("urllib_parse"),
            expected
        )
        expected = {
            "type": "MovedModule",
            "value": ("urllib_parse", "six.moves.urllib_parse", "urllib.parse")
        }
        self.assertEqual(
            self.compat.lookup("six.moves.urllib_parse"),
            expected
        )
        expected = {
            "type": "MovedAttribute",
            "value": ("cStringIO", "cStringIO", "io", "StringIO")

        }
        self.assertEqual(
            self.compat.lookup("six.StringIO"),
            expected
        )
