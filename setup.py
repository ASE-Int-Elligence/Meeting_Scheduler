#!/usr/bin/env python

from distutils.core import setup
from glob import glob
import os

from setuptools import find_packages

setup(name='Meeting_Scheduler',
      version='0.1',
      description='Application that helps users schedule meetings',
      author='Chandana, Jiayi, Srujan, Varun',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
)