# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import matplotlib

setup(console=['Vent.py'],
      data_files=matplotlib.get_py2exe_datafiles())