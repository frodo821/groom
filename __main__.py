# encoding: utf-8
"""
groom

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

import sys
import unittest
from . import *

__version__ = '0.0.1'

def function(*,
  first_arg: positional(int, 'int value', required=True, var_name='INT'),
  second_arg: switch('switch value', short_name='s'),
  third_arg: optional(str, 'string value', short_name='t') = 'string',
  fourth_arg: multiple(float, 'list of float values', short_name='f') = [0.1, 3.2]):
  print('first_arg:', first_arg)
  print('second_arg:', second_arg)
  print('third_arg:', third_arg)
  print('fourth_arg:', fourth_arg)

class DispatcherTest(unittest.TestCase):
  def setUp(self):
    self.disp = Dispatcher(
      function,
      "A test command-line program.")

  def test_helpmsg(self):
    sys.argv = [sys.argv[0], '-h']
    with self.assertRaises(SystemExit):
      self.disp.dispatch()

  def test_version(self):
    sys.argv = [sys.argv[0], '-v']
    with self.assertRaises(SystemExit):
      self.disp.dispatch()

  def test_positional(self):
    sys.argv = [sys.argv[0], '2']
    self.disp.dispatch()

  def test_keyword_switch(self):
    sys.argv = [sys.argv[0], '2', '--second-arg']
    self.disp.dispatch()

  def test_keyword_switch_short(self):
    sys.argv = [sys.argv[0], '2', '-s']
    self.disp.dispatch()

  def test_multiple_argument(self):
    sys.argv = [sys.argv[0], '2', '-f', '0.2', '-f', '0.5']
    self.disp.dispatch()

  def test_invaild_argument(self):
    sys.argv = [sys.argv[0], '--invalid']
    with self.assertRaises(SystemExit):
      self.disp.dispatch()

unittest.main()
