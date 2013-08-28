#!/usr/bin/env python
#--coding: utf8--

import sys
import os.path

import pygit2
from pyscrum.loaders import RstLoader

filename = sys.argv[1]
repo = pygit2.Repository(os.path.dirname(filename))
