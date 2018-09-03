# -*- coding: utf-8 -*-
"""
project desc
"""

# import os
import pkgutil

__version__ = pkgutil.get_data(__package__, 'VERSION').decode('ascii').strip()

__author__ = "hyxf"
