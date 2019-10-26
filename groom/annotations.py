# encoding: utf-8
"""
annotations.py

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

class Annotation:
  def __init__(
      self, type_, desc='', *,
      allow_multiple=False,
      positional=False,
      short_name=None,
      required=False,
      var_name=None):
    if not isinstance(type_, type):
      raise TypeError(f"'{type(type_).__name__}' class is not inherits type class.")
    if type_ not in (str, int, float, complex, bool):
      raise TypeError(f"'{type_.__name__}' is not applicable type.")
    if type_ is bool and positional:
      raise TypeError("switch args can't be positional args.")
    self.type = type_
    self.desc = desc
    self.allow_multiple = allow_multiple
    self.positional = positional
    self.short_name = short_name
    self.required = required
    self.var_name = var_name

def positional(type, desc='', *, required=False, var_name=None):
  """
  Annotation for positional arguments.
  """
  return Annotation(
    type, desc,
    positional=True,
    required=required,
    var_name=var_name)

def optional(type, desc='', *, var_name=None, short_name=None):
  """
  Annotation for keyword-only optional arguments.
  """
  return Annotation(
    type, desc,
    var_name=var_name,
    short_name=short_name)

def multiple(type, desc='', *, required=False, var_name=None, short_name=None):
  """
  Annotation for keyword-only list arguments.
  """
  return Annotation(
    type, desc,
    allow_multiple=True,
    required=required,
    var_name=var_name,
    short_name=short_name)

def required(type, desc='', *, var_name=None, short_name=None):
  """
  Annotation for keyword-only required arguments.
  """
  return Annotation(
    type, desc,
    required=True,
    var_name=var_name,
    short_name=short_name)

def switch(desc='', *, short_name=None):
  """
  Annotation for switch arguments.
  """
  return Annotation(
    bool, desc, short_name=short_name)
