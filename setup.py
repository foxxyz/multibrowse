# Setup script for use with py2exe
from distutils.core import setup
import py2exe
from multibrowse import __version__

setup(console=[
	{
		'script': 'multibrowse.py',
		'dest_base': 'multibrowse_{}'.format(__version__)
	}], zipfile=None, options={"py2exe":{"bundle_files": 1, "includes": ["systems.linux", "systems.win"]}})