# encoding: utf-8
# type: ignore
"""
groom

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

import sys
import unittest
from .annotations import multiple, optional, positional, required, switch
from .dispatching import Dispatcher, entrypoint
from typing import Type

__version__ = '0.0.4a1'


@entrypoint("A test command-line program.")
def function(
    *,
    first_arg: switch('switch value', short_name='s'),
    second_arg: optional(str, 'string value', short_name='t') = 'string',
        third_arg: multiple(float, 'list of float values', short_name='f') = [0.1, 3.2]):
  print('first_arg:', first_arg)
  print('second_arg:', second_arg)
  print('third_arg:', third_arg)


function.dispatch()

# @function.subcommand("subcmd", "A test sub command")
# def sub_function(
#     *,
#     first_arg: positional(int, 'int value', required=True, var_name='INT'),
#     second_arg: switch('switch value', short_name='s'),
#     third_arg: optional(str, 'string value', short_name='t') = 'string',
#         fourth_arg: multiple(float, 'list of float values', short_name='f') = [0.1, 3.2]):
#   print('first_arg:', first_arg)
#   print('second_arg:', second_arg)
#   print('third_arg:', third_arg)
#   print('fourth_arg:', fourth_arg)


# @sub_function.subcommand("dummy", "A dummy sub command")
# def dummy(
#     *,
#     first_arg: switch('switch value', short_name='s'),
#     second_arg: optional(str, 'string value', short_name='t') = 'string',
#         third_arg: multiple(float, 'list of float values', short_name='f') = [0.1, 3.2]):
#   print('first_arg:', first_arg)
#   print('second_arg:', second_arg)
#   print('third_arg:', third_arg)


# @dummy.subcommand("subcmd", "A dummy sub-sub command")
# def dummy_sub(
#     *,
#     first_arg: positional(int, 'int value', required=True, var_name='INT'),
#     second_arg: switch('switch value', short_name='s'),
#     third_arg: optional(str, 'string value', short_name='t') = 'string',
#         fourth_arg: multiple(float, 'list of float values', short_name='f') = [0.1, 3.2]):
#   print('first_arg:', first_arg)
#   print('second_arg:', second_arg)
#   print('third_arg:', third_arg)
#   print('fourth_arg:', fourth_arg)


# class DispatcherTest(unittest.TestCase):
#   def setUp(self):
#     self.disp = function

#   def test_helpmsg(self):
#     sys.argv = [sys.argv[0], '-h']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_version(self):
#     sys.argv = [sys.argv[0], '-v']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_positional(self):
#     sys.argv = [sys.argv[0], 'subcmd', '2']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_required_positional_not_specify(self):
#     sys.argv = [sys.argv[0], 'subcmd']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_keyword_switch(self):
#     sys.argv = [sys.argv[0], '--first-arg']
#     self.disp.dispatch()

#   def test_keyword_switch_short(self):
#     sys.argv = [sys.argv[0], '-s']
#     self.disp.dispatch()

#   def test_multiple_argument(self):
#     sys.argv = [sys.argv[0], '-f', '0.2', '-f', '0.5']
#     self.disp.dispatch()

#   def test_subcommand(self):
#     sys.argv = [sys.argv[0], 'subcmd', '2']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_unknown_subcommand(self):
#     sys.argv = [sys.argv[0], 'subcmd1']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()

#   def test_invaild_argument(self):
#     sys.argv = [sys.argv[0], '--invalid']
#     with self.assertRaises(SystemExit):
#       self.disp.dispatch()


# unittest.main()
