#!/usr/bin/env python3
"""
Optimized PyInstaller spec for minimal size Video Editor
"""

import sys
from pathlib import Path

PROJECT_DIR = Path.cwd()
SITE_PACKAGES = Path(sys.executable).parent / "Lib" / "site-packages"
PYSIDE6_DIR = SITE_PACKAGES / "PySide6"

# Modules to EXCLUDE (not used by our app)
EXCLUDES = [
    # PySide6 modules we don't use
    'PySide6.Qt3DAnimation', 'PySide6.Qt3DCore', 'PySide6.Qt3DExtras',
    'PySide6.Qt3DInput', 'PySide6.Qt3DLogic', 'PySide6.Qt3DRender',
    'PySide6.QtAsyncio', 'PySide6.QtAxContainer', 'PySide6.QtBluetooth',
    'PySide6.QtCharts', 'PySide6.QtConcurrent', 'PySide6.QtDBus',
    'PySide6.QtDataVisualization', 'PySide6.QtDesigner', 'PySide6.QtGraphs',
    'PySide6.QtGraphsWidgets', 'PySide6.QtHelp', 'PySide6.QtHttpServer',
    'PySide6.QtLocation', 'PySide6.QtMultimedia', 'PySide6.QtMultimediaWidgets',
    'PySide6.QtNetworkAuth', 'PySide6.QtNfc', 'PySide6.QtOpenGL',
    'PySide6.QtOpenGLWidgets', 'PySide6.QtPdf', 'PySide6.QtPdfWidgets',
    'PySide6.QtPositioning', 'PySide6.QtPrintSupport', 'PySide6.QtQml',
    'PySide6.QtQuick', 'PySide6.QtQuick3D', 'PySide6.QtQuickControls2',
    'PySide6.QtQuickTest', 'PySide6.QtQuickWidgets', 'PySide6.QtRemoteObjects',
    'PySide6.QtScxml', 'PySide6.QtSensors', 'PySide6.QtSerialBus',
    'PySide6.QtSerialPort', 'PySide6.QtSpatialAudio', 'PySide6.QtSql',
    'PySide6.QtStateMachine', 'PySide6.QtSvg', 'PySide6.QtSvgWidgets',
    'PySide6.QtTest', 'PySide6.QtTextToSpeech', 'PySide6.QtUiTools',
    'PySide6.QtWebChannel', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineQuick',
    'PySide6.QtWebEngineWidgets', 'PySide6.QtWebSockets', 'PySide6.QtWebView',
    'PySide6.QtXml', 'PySide6.QtXmlPatterns',
    'PySide6.scripts', 'PySide6.support', 'PySide6._config',
    
    # Standard library modules we don't need
    'matplotlib', 'scipy', 'pandas', 'PIL', 'Pillow',
    'notebook', 'IPython', 'jupyter', 'jupyter_client', 'jupyter_core',
    'qtconsole', 'spyder', 'pylint', 'black', 'ruff', 'mypy',
    'pytest', 'pytest_qt', 'setuptools', 'wheel', 'pip', 'pkg_resources',
    'distutils', 'ensurepip', 'venv', 'virtualenv',
    'tkinter', 'turtle', 'idlelib', 'pydoc', 'doctest',
    'unittest', 'test', 'pdb', 'profile', 'cProfile',
    'http', 'html', 'xmlrpc', 'urllib', 'email', 'mailbox',
    'mimetypes', 'base64', 'binascii', 'quopri', 'uu',
    'hashlib', 'hmac', 'secrets', 'uuid', 'random', 'statistics',
    'fractions', 'decimal', 'numbers', 'math', 'cmath',
    'itertools', 'functools', 'operator', 'collections', 'heapq',
    'bisect', 'array', 'weakref', 'types', 'copy', 'pprint',
    'reprlib', 'enum', 'graphlib', 'dataclasses', 'typing',
    'string', 'textwrap', 'difflib', 'stringprep', 'readline',
    'rlcompleter', 'cmd', 'shlex', 'getopt', 'argparse', 'optparse',
    'subprocess', 'sched', 'queue', 'threading', 'multiprocessing',
    'concurrent', 'contextvars', 'asyncio', 'selectors', 'select',
    'socket', 'ssl', 'signal', 'mmap', 'fcntl', 'termios', 'pty',
    'resource', 'syslog', 'logging', 'warnings', 'traceback',
    'linecache', 'pickle', 'shelve', 'marshal', 'dbm', 'sqlite3',
    'csv', 'configparser', 'netrc', 'xdrlib', 'plistlib',
    'json', 'tomllib', 'xml', 'yaml', 'html', 'webbrowser',
    'cgi', 'cgitb', 'wsgiref', 'http', 'urllib', 'ftplib',
    'poplib', 'imaplib', 'nntplib', 'smtplib', 'email', 'mailcap',
    'mailbox', 'mimetypes', 'base64', 'binhex', 'uu', 'quopri',
    'colorsys', 'imghdr', 'sndhdr', 'wave', 'aifc', 'sunau',
    'au', 'chunk', 'ossaudiodev', 'spwd', 'grp', 'pwd', 'crypt',
    'termios', 'tty', 'pty', 'fcntl', 'pipes', 'shlex', 'shutil',
    'tempfile', 'glob', 'fnmatch', 'linecache', 'dircache', 'stat',
    'filecmp', 'macpath', 'os', 'os.path', 'posixpath', 'ntpath',
]

# Modules to INCLUDE explicitly (hidden imports)
HIDDEN_IMPORTS = [
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui', 
    'PySide6.QtWidgets',
    'shiboken6',
    'av',
    'av.codec',
    'av.container',
    'av.format',
    'av.filter',
    'av.video',
    'av.audio',
    'numpy',
    'numpy.core',
    'numpy.lib',
    'cv2',
    'cv2.cv2',
]

# Binary dependencies (DLLs) to include - use actual paths
BINARIES = []
PLUGIN_DIRS = [
    'platforms', 'styles', 'imageformats', 'iconengines',
    'mediaservice', 'playlists', 'audio', 'video',
    'generic', 'sceneparser', 'gamepads', 'geometryloaders',
    'geoservices', 'printsupport', 'renderplugins',
    'renderers', 'scenefileformat', 'sqldrivers',
    'texttospeech', 'themeplugins', 'tls', 'virtualkeyboard',
    'webview', 'xcbglintegrations',
]

for plugin_dir in PLUGIN_DIRS:
    src_dir = PYSIDE6_DIR / "plugins" / plugin_dir
    if src_dir.exists():
        for dll in src_dir.glob("*.dll"):
            BINARIES.append((str(dll), f"PySide6/plugins/{plugin_dir}"))

# Data files to include
DATAS = [
    ('core', 'core'),
    ('render', 'render'),
    ('ui', 'ui'),
    ('plugins', 'plugins'),
    ('resources/icon.ico', 'resources'),
    ('README.md', '.'),
]

# Analysis configuration
a = Analysis(
    ['main.py'],
    pathex=[str(PROJECT_DIR)],
    binaries=BINARIES,
    datas=DATAS,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDES,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Filter out unnecessary binaries
a.binaries = [
    (dest, src, typ) for dest, src, typ in a.binaries
    if not any(x in src.lower() for x in [
        'qtwebengine', 'qtwebchannel', 'qtwebview', 'qtquick', 'qtqml',
        'qt3d', 'qtcharts', 'qtdatavis', 'qtnetworkauth', 'qtnfc',
        'qtpositioning', 'qtprintsupport', 'qtremoteobjects', 'qtscxml',
        'qtsensors', 'qtserialbus', 'qtserialport', 'qtspatialaudio',
        'qtsql', 'qtstatemachine', 'qtsvg', 'qttest', 'qttexttospeech',
        'qtuitools', 'qtweb', 'qtxml', 'qtxmlpatterns',
        'opengl', 'multimedia', 'bluetooth', 'nfc', 'positioning',
        'webengine', 'webchannel', 'webview', 'quick', 'qml',
        'designer', 'help', 'location', 'charts', 'datavis', 'graphs',
    ])
]

# Filter out unnecessary datas
a.datas = [
    (dest, src, typ) for dest, src, typ in a.datas
    if not any(x in src.lower() for x in [
        '__pycache__', '.pyc', '.pyo', '.pyd', '.dist-info', '.egg-info',
        'test', 'tests', 'doc', 'docs', 'example', 'examples', 'demo',
    ])
]

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='video_editor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico',
)