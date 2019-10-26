Groom
=====

A easy-to-use command-line interface generator

introduction
------------

Have you never wanted to create cli tools with python more easily?
Groom brings you easier way to create cli tools.

Here is an example:

.. code-block:: python

  from groom import *

  def function(*,
    first_arg: positional(
      int,
      'int value',
      required=True,
      var_name='INT'),
    second_arg: switch(
      'switch value',
      short_name='s'),
    third_arg: optional(
      str,
      'string value',
      short_name='t') = 'string',
    fourth_arg: multiple(
      float,
      'list of float values',
      short_name='f') = [0.1, 3.2]):
    print('first_arg:', first_arg)
    print('second_arg:', second_arg)
    print('third_arg:', third_arg)    
    print('fourth_arg:', fourth_arg)

  if __name__ == '__main__':
    Dispatcher(
      function,
      "A test command-line program"
    ).dispatch()

This supports int, str, float, complex, and bool as a parameter type.
If you passed other types, it will throw TypeError.

Features
--------
Groom has those features:

* default values
* list parameters
* automatic help generation
* sub-command support
