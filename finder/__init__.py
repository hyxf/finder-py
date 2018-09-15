# -*- coding: utf-8 -*-
"""
project desc
"""
import pkgutil
import sys

__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()

__author__ = "hyxf"

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)
