modules = """Please wait a moment while I gather a list of all available modules...

PIL                 _weakrefset         http                select
__future__          _xxsubinterpreters  idlelib             selectors
_abc                _xxtestfuzz         if_else             setuptools
_aix_support        _yaml               imaplib             shelve
_ast                _zoneinfo           imghdr              shlex
_asyncio            abc                 imp                 shutil
_bisect             aifc                importlib           signal
_blake2             antigravity         iniconfig           simple_calculator
_bootsubprocess     argcomplete         inspect             site
_bz2                argparse            io                  smtpd
_codecs             array               ipaddress           smtplib
_codecs_cn          asciimatics         isort               sndhdr
_codecs_hk          ast                 itertools           socket
_codecs_iso2022     asynchat            json                socketserver
_codecs_jp          asyncio             keyword             sqlite3
_codecs_kr          asyncore            lib2to3             sre_compile
_codecs_tw          atexit              linecache           sre_constants
_collections        audioop             lists               sre_parse
_collections_abc    base64              locale              ssl
_compat_pickle      bdb                 logging             stat
_compression        binascii            lookatme            statistics
_contextvars        binhex              lzma                string
_crypt              bisect              mailbox             stringprep
_csv                builtins            mailcap             struct
_ctypes             bz2                 markdown_it         subprocess
_ctypes_test        cProfile            marshal             sunau
_curses             calendar            marshmallow         symtable
_curses_panel       cgi                 math                sys
_datetime           cgitb               mdurl               sysconfig
_dbm                chunk               mimetypes           syslog
_decimal            click               mistune             tabnanny
_distutils_hack     cmath               mmap                tarfile
_elementtree        cmd                 modulefinder        telnetlib
_functools          code                multiprocessing     tempfile
_gdbm               codecs              netrc               termios
_hashlib            codeop              newbie03            test
_heapq              collections         newbie04            test_calc
_imp                colorsys            nis                 textwrap
_io                 compare_movies      nntplib             this
_json               compileall          ntpath              threading
_locale             concurrent          nturl2path          three_questions
_lsprof             configparser        numbers             three_questions_funcs
_lzma               contextlib          opcode              time
_markupbase         contextvars         operator            timeit
_md5                copy                optparse            tkinter
_multibytecodec     copyreg             os                  token
_multiprocessing    crypt               packaging           tokenize
_opcode             csv                 pathlib             tomli
_operator           ctypes              pdb                 trace
_osx_support        curses              pickle              traceback
_pickle             dad_jokes           pickletools         tracemalloc
_posixshmem         dataclasses         pip                 truthy
_posixsubprocess    datetime            pipes               tty
_py_abc             dbm                 pipx                turtle
_pydecimal          decimal             pkg_resources       turtledemo
_pyio               dictionaries        pkgutil             types
_pytest             difflib             platform            typing
_queue              dis                 plistlib            typing_extensions
_random             distutils           pluggy              unicodedata
_scproxy            doctest             poplib              unittest
_sha1               email               posix               urllib
_sha256             encodings           posixpath           urwid
_sha3               ensurepip           pprint              userpath
_sha512             enum                present             uu
_signal             errno               profile             uuid
_sitebuiltins       errors              pstats              venv
_socket             exceptiongroup      pty                 warnings
_sqlite3            faulthandler        pwd                 wave
_sre                fcntl               py                  wcwidth
_ssl                filecmp             py_compile          weakref
_stat               fileinput           pyclbr              webbrowser
_statistics         fnmatch             pydoc               wheel
_string             fractions           pydoc_data          while
_strptime           ftplib              pyexpat             while_loops
_struct             funcs               pyfiglet            wsgiref
_symtable           functools           pygments            xdrlib
_sysconfigdata__darwin_darwin gc                  pytest              xml
_testbuffer         genericpath         queue               xmlrpc
_testcapi           getopt              quopri              xxlimited
_testimportmultiple getpass             random              xxlimited_35
_testinternalcapi   gettext             re                  xxsubtype
_testmultiphase     glob                readline            yaml
_thread             graphlib            reprlib             zipapp
_threading_local    grp                 resource            zipfile
_tkinter            gzip                rich                zipimport
_tracemalloc        hashlib             rlcompleter         zlib
_uuid               heapq               runpy               zoneinfo
_warnings           hmac                sched
_weakref            html                secrets

Enter any module name to get more help.  Or, type "modules spam" to search
for modules whose name or summary contain the string "spam"."""


lines = modules.splitlines()

count = 0
for line in lines[1:-2]:
    count += len(line.split())

print(count)
