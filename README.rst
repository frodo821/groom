Groom
=====

Groom, is an easy-to-use command-line application framework.

This module defines an even much easier way to make user-friendly command-line interfaces than any others else.
Once you define a function as the entry point of your application, Groom will automatically detect how to parse ``sys.argv`` and apply it to your application. 
Groom also generates help and usage messages and issue errors when users set invalid arguments to your application. 

introduction
------------

Have you never wanted to create CLI tools with python more easily?
Groom brings you an easier way to create CLI tools.

Here is an example:

.. code-block:: python

    import sys
    from groom import positional, optional, Dispatcher
    
    __version__ = '1.0'
    
    def calculate(
        num1: positional(float, "former number", required=True, var_name='N1'),
        num2: positional(float, "latter number", required=True, var_name='N2'),
        operator: optional(str, "operator name", short_name='op')='add'):
      if operator == 'add':
        print(num1 + num2)
        return
      if operator == 'sub':
        print(num1 - num2)
        return
      if operator == 'mul':
        print(num1 * num2)
        return
      if operator == 'div':
        print(num1 / num2)
        return
      print("unknown operator:", operator, file=sys.stderr)
    
    if __name__ == '__main__':
      Dispatcher(
        calculate,
        "calculate one of four arithmetic operations"
      ).dispatch()

...and then, you can call the program like this:

.. code-block:: sh

    $ python calc.py 1 2 -op div

Once you call this program with ``-h`` or ``--help``, Groom displays the help messages:

.. code-block:: sh

    $ python calc.py -h
    calc.py: 1.0
    
    calculate one of four arithmetic operations
    
    Usage:
      calc.py [-v | --version | -h | --help]
      calc.py <N1> <N2>
        [--operator <OPERATOR> | -op <OPERATOR>]
    
    positional parameters:
    N1:
      former number
      type: float
      required: True
    N2:
      latter number
      type: float
      required: True
    
    parameters:
    --operator, -op:
      operator name
      type: str
      required: False
      multiple values: False
      default: add

Groom can handle 6 primitive types such as str, int, float, complex and bool and list of those types.
If you specify another as a parameter type, Groom will throw TypeError.

Groom is licensed under the MIT License, for further details see LICENSE.txt.
