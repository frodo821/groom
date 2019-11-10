""""""
#  setup.py
#
#  Created by Frodo on 6/10/2019
#  Copyright (c) 2019 Frodo.

from os.path import dirname, abspath
from setuptools import setup, find_packages

try:
  with open("README.rst") as f:
    readme = f.read()
except IOError:
  readme = ""

here = dirname(abspath(__file__))
version = '0.0.3a2'

setup(
  name="groom",
  version=version,
  url="https://github.com/frodo821/groom",
  author="frodo821 <Twitter: @BoufrawFrodo2>",
  author_email='1234567890.sakai.jp@gmail.com',
  maintainer="frodo821 <Twitter: @BoufrawFrodo2>",
  maintainer_email='1234567890.sakai.jp@gmail.com',
  description="A easy-to-use command-line interface generator",
  long_description=readme,
  packages=find_packages(),
  install_requires=[],
  license="MIT",
  classifiers=[
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Topic :: Utilities',
    'Topic :: Terminals',
    'Topic :: Software Development :: Libraries :: Application Frameworks'
  ],
  entry_points="")
