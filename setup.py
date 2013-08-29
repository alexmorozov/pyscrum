#!/usr/bin/env python
#--coding: utf8--

from setuptools import setup

setup(name='pyscrum',
      version='0.2',
      description='Generate scrum boards and charts from .rst task logs.',
      long_description=open('README.rst').read(),
      author='Alex Morozov',
      author_email='inductor2000@mail.ru',
      url='http://github.com/alexmorozov/pyscrum',
      license='GPLv3',
      packages=['pyscrum'],
      requires=['docutils', 'jinja2'],
      scripts=['tools/mkboard.py', 'tools/mkburndown.py']
     )
