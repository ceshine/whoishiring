#!/usr/bin/python
from setuptools import setup, find_packages


setup(name='whoishiring',
      version='0.1.0',
      author='Jan Zegan',
      description='Get job posts from hn',
      author_email='jzegan@gmail.com',
      url="https://github.com/joshz/whoishiring",
      install_requires=['pip', 'lxml', 'pyquery', 'python-dateutil'],
      packages=find_packages(exclude=["tests*"])
      )