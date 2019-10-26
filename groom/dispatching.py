# encoding: utf-8
"""
dispatching.py

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

import sys
from os.path import basename
from inspect import signature as sig, Parameter
from .annotations import Annotation

__all__ = ["Dispatcher"]

def to_param_name(name):
  return f"--{name.lower().replace('_', '-')}"

def get_program_name():
  p = __package__ or sys.argv[0]
  return basename(p)

class Dispatcher:
  """
  Dispatches command-line call to python function call.

  Parameters:

  * func: a function to call
  * desc: tool description
  """
  def __init__(self, func=None, desc=None, *, is_subcommand=False):
    self.func = func
    self.desc = desc
    self.is_subcommand = is_subcommand
    self.subdisps = {}
    self.keywords = {}
    self.defaults = {}
    self.positionals = []
    if self.func is None:
      return
    for n, p in sig(func).parameters.items():
      ann = p.annotation
      if ann is Parameter.empty:
        raise ValueError(f"parameter '{n}' is not annotated.")
      if not isinstance(ann, Annotation):
        raise TypeError(f"unexpected annotation type: {type(ann).__name__}")
      self.defaults[n] = p.default if p.default is not Parameter.empty else None
      if ann.positional:
        self.positionals.append((n, ann))
        continue
      self.keywords[to_param_name(n)] = n, ann
      if ann.short_name:
        self.keywords[f"-{ann.short_name}"] = n, ann
    self.positionals.sort(key=lambda x: not x[1].required)

  def dispatch(self):
    """
    Dispatches command-line call to python function call.
    """
    params = {}
    pos = iter(self.positionals)
    pac = 0
    idx = 1
    while sys.argv[idx:]:
      arg = sys.argv[idx]
      if arg in ('-h', '--help'):
        print(self.helpmsg())
        sys.exit(0)
      if arg in ('-v', '--version'):
        import __main__ as m
        print(f"{get_program_name()}: {getattr(m, '__version__', 'UNVERSIONED')}")
        sys.exit(0)
      if not arg.startswith('-'):
        if idx == 1 and self.subdisps:
          sd = self.subdisps.get(arg)
          if sd is None:
            print((
              f"unexpected subcommand: '{arg}'\n"
              "please try execute this command with '-h' or '--help' to get helps."),
              file=sys.stderr)
            sys.exit(-1)
          sys.argv.pop(0)
          return sd.dispatch()
        try:
          n, p = next(pos)
        except:
          print((
            f"unexpected argument: '{arg}'\n"
            "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
          sys.exit(-1)
        try:
          params[n] = p.type(arg)
        except:
          print((
            f"invalid literal '{arg}' for type '{p.type.__name__}'\n"
            "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
          exit(-1)
        idx += 1
        continue
      try:
        n, p = self.keywords.get(arg)
      except TypeError:
        print((
          f"unexpected argument: '{arg}'\n"
          "please try execute this command with '-h' or '--help' to get helps."),
          file=sys.stderr)
        sys.exit(-1)
      if p.allow_multiple and n not in params:
        params[n] = []
      if p.type is bool:
        params[n] = True
        idx += 1
        continue
      try:
        v = p.type(sys.argv[idx+1])
      except IndexError:
        print((
          f"no value passed for parameter '{arg}'\n"
          "please try execute this command with '-h' or '--help' to get helps."),
          file=sys.stderr)
        sys.exit(-1)
      except:
        print((
          f"invalid literal '{arg}' for type '{p.type.__name__}'\n"
          "please try execute this command with '-h' or '--help' to get helps."),
          file=sys.stderr)
        exit(-1)
      if p.allow_multiple:
        params[n].append(v)
      else:
        params[n] = v
      idx += 2
    for name, param in self.positionals:
      if name not in params:
        if param.required:
          print((
            f"some of required positional parameter was not specified.\n"
            "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
          sys.exit(-1)
        params[name] = self.defaults[name]
    for name, param in self.keywords.values():
      if name not in params:
        if param.required:
          print((
            f"required parameter '{to_param_name(name)}' was not specified.\n"
            "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
          sys.exit(-1)
        if param.type is bool:
          params[name] = False
          continue
        params[name] = self.defaults[name]
    self.func(**params)

  def helpmsg(self):
    """
    Generate help message
    """
    import __main__ as m
    pn = get_program_name()
    ret = [
      self.desc
    ] if self.is_subcommand else [
      f"{pn}: {getattr(m, '__version__', 'UNVERSIONED')}",
      "",
      self.desc,
      "",
      "Usage:",
      f"  {pn} [-v | --version | -h | --help]"
    ]
    if self.subdisps:
      if not self.is_subcommand:
        ret.append(f"  {pn} subcommand params...")
        ret.append("")
      ret.append("subcommands:")
      for sn, sc in self.subdisps:
        ret.append(f"{sn}:")
        ret.append(sc.helpmsg().replace('\n', '\n  '))
    else:
      ret.append(f"  {pn} params...")
      ret.append("")
      ret.append("positional parameters:")
      for n, p in self.positionals:
        ret.append(f"{p.var_name or n.upper()}:")
        ret.append(f"  {p.desc}")
        ret.append(f"  type: {p.type.__name__}")
        ret.append(f"  required: {p.required}")
        if not p.required:
          ret.append(f"  default: {self.defaults[n]}")
      ret.append("")
      ret.append("parameters:")
      for word, (n, p) in self.keywords.items():
        if not word.startswith('--'):
          continue
        ret.append(f"{word + (f', -{p.short_name}' if p.short_name else '')}:")
        ret.append(f"  {p.desc}")
        ret.append(f"  type: {p.type.__name__}")
        ret.append(f"  required: {p.required}")
        ret.append(f"  multiple values: {p.allow_multiple}")
        if not p.required:
          ret.append(f"  default: {self.defaults[n]}")
      return '\n'.join(ret)

  def add_subcommand(self, name, dispatcher):
    """
    Add a dispatcher as a sub-command.
    """
    dispatcher.is_subcommand = True
    self.subdisps[name] = dispather
