# Setup script for use with py2exe
from distutils.core import setup
import py2exe

setup(console=['multibrowse.py'], zipfile=None, options={"py2exe":{"bundle_files": 1, "includes": ["systems.linux", "systems.win"]}})