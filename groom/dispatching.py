# encoding: utf-8
"""
dispatching.py

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

import sys
from os.path import basename
from inspect import signature as sig, Parameter
from typing import List, Dict, Tuple, Union

from .annotations import Annotation

__all__ = ["Dispatcher"]

_Param = Union[str, float, int, complex, bool]

def _to_param_name(name):
  return f"--{name.lower().replace('_', '-')}"

def _get_program_name():
  from __main__ import __package__ as pkg
  p = pkg or sys.argv[0]
  return basename(p)

def _generate_disp_info(func) -> Tuple[Dict[str, _Param], Dict[str, Annotation], List[Annotation]]:
  defaults, keywords, positionals = {}, {}, []
  for n, p in sig(func).parameters.items():
    ann = p.annotation
    if ann is Parameter.empty:
      raise ValueError(f"parameter '{n}' is not annotated.")
    if not isinstance(ann, Annotation):
      raise TypeError(f"unexpected annotation type: {type(ann).__name__}")
    defaults[n] = p.default if p.default is not Parameter.empty else None
    if ann.positional:
      positionals.append((n, ann))
      continue
    keywords[_to_param_name(n)] = n, ann
    if ann.short_name:
      keywords[f"-{ann.short_name}"] = n, ann
  positionals.sort(key=lambda x: not x[1].required)
  return defaults, keywords, positionals

class Dispatcher:
  """
  Dispatches command-line call to python function call.

  Parameters:

  * func: a function to call
  * desc: tool description
  """
  positionals: List[Annotation]
  keywords: Dict[str, Annotation]
  defaults: Dict[str, _Param]

  def __init__(self, func=None, desc: str = None, *, is_subcommand: bool = False):
    self.func = func
    self.desc = desc
    self.is_subcommand = is_subcommand
    self.subdisps = {}
    if self.func is None:
      return
    self.defaults, self.keywords, self.positionals = _generate_disp_info(func)

  def __check_default_action(self, arg):
    if arg in ('-h', '--help'):
      print(self.helpmsg())
      sys.exit(0)
    if arg in ('-v', '--version'):
      import __main__ as m
      print(f"{_get_program_name()}: {getattr(m, '__version__', 'UNVERSIONED')}")
      sys.exit(0)

  def __handle_not_keyword(self, arg, idx, pos, params):
    if idx == 1 and self.subdisps:
      sd = self.subdisps.get(arg)
      if sd is None:
        print((f"unexpected subcommand: '{arg}'\n"
               "please try execute this command with '-h' or '--help' to get helps."),
              file=sys.stderr)
        sys.exit(-1)
      sys.argv.pop(0)
      sd.dispatch()
      sys.exit(0)
    try:
      n, p = next(pos)
    except StopIteration:
      print((f"unexpected argument: '{arg}'\n"
             "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
      sys.exit(-1)
    try:
      params[n] = p.type(arg)
    except ValueError:
      print((f"invalid literal '{arg}' for type '{p.type.__name__}'\n"
             "please try execute this command with '-h' or '--help' to get helps."),
            file=sys.stderr)
      exit(-1)

  def __post_validate(self, params):
    for name, param in self.positionals:
      if name not in params:
        if param.required:
          print((f"some of required positional parameter was not specified.\n"
                 "please try execute this command with '-h' or '--help' to get helps."),
                file=sys.stderr)
          sys.exit(-1)
        params[name] = self.defaults[name]
    for name, param in self.keywords.values():
      if name not in params:
        if param.required:
          print((f"required parameter '{_to_param_name(name)}' was not specified.\n"
                 "please try execute this command with '-h' or '--help' to get helps."),
                file=sys.stderr)
          sys.exit(-1)
        if param.type is bool:
          params[name] = False
          continue
        params[name] = self.defaults[name]

  def dispatch(self):
    """
    Dispatches command-line call to python function call.
    """
    params = {}
    pos = iter(self.positionals)
    idx = 1
    while sys.argv[idx:]:
      arg = sys.argv[idx]
      self.__check_default_action(arg)
      if not arg.startswith('-'):
        self.__handle_not_keyword(arg, idx, pos, params)
        idx += 1
        continue
      try:
        n, p = self.keywords.get(arg)
      except TypeError:
        print((f"unexpected argument: '{arg}'\n"
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
        print((f"no value passed for parameter '{arg}'\n"
               "please try execute this command with '-h' or '--help' to get helps."),
              file=sys.stderr)
        sys.exit(-1)
      except ValueError:
        print(
          (f"invalid literal '{arg}' for type '{p.type.__name__}'\n"
           "please try execute this command with '-h' or '--help' to get helps."),
          file=sys.stderr)
        exit(-1)
      if p.allow_multiple:
        params[n].append(v)
      else:
        params[n] = v
      idx += 2
    self.__post_validate(params)
    self.func(**params)

  def __generate_usage(self, name, sub_names=[]):
    ret = []
    ps = []
    for n, p in self.positionals:
      ps.append(f"<{p.var_name}>" if p.required else f"[{p.var_name or n.upper()}]")
    ret.append(' '.join(ps))
    for arg, (n, p) in filter(lambda x: x[0].startswith('--'), self.keywords.items()):
      ret.append(f"    {p.display(arg, n)}")
    args = '\n'.join(ret).strip()
    sn = ' '.join(sub_names)
    return f"  {name}{f' {sn}' if self.is_subcommand else ''} {args}"

  def helpmsg(self, sub_names=[]):
    """
    generate help message
    """
    import __main__ as m
    pn = _get_program_name()
    ret = [
      "",
      self.desc,
      ""
    ] if self.is_subcommand else [
      f"{pn}: {getattr(m, '__version__', 'UNVERSIONED')}",
      "",
      self.desc,
      "",
      "Usage:",
      f"  {pn} [-v | --version | -h | --help]"
    ]
    ret.append(self.__generate_usage(pn, sub_names))
    ret.append("")

    if self.positionals:
      ret.append("")
      ret.append("positional parameters:")
      for n, p in self.positionals:
        ret.append(f"{p.var_name or n.upper()}:")
        ret.append(f"  {p.desc}")
        ret.append(f"  type: {p.type.__name__}")
        ret.append(f"  required: {p.required}")
        if not p.required:
          ret.append(f"  default: {self.defaults[n]}")

    if self.keywords:
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

    if self.subdisps:
      if not self.is_subcommand:
        ret.append(f"  {pn} subcommand params...")
        ret.append("")
      ret.append("subcommands:")
      for sn, sc in self.subdisps.items():
        ret.append("")
        ret.append(f"{sn}:")
        ret.append(sc.helpmsg(sub_names=sub_names + [sn]).replace('\n', '\n  '))

    return '\n'.join(ret)

  def add_subcommand(self, name, dispatcher):
    """
    Add a dispatcher as a sub-command.
    """
    dispatcher.is_subcommand = True
    self.subdisps[name] = dispatcher
