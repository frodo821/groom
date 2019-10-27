# encoding: utf-8
"""
groom

Created by Frodo on 10/26/19.
Copyright (c) 2019 Frodo. All rights reserved.
"""

from .annotations import (
  positional, optional,
  multiple, required, switch)
from .dispatching import Dispatcher

__all__ = [
  "positional", "optional",
  "multiple", "required",
  "switch", "Dispatcher"
]

__version__ = "0.0.3a1"
