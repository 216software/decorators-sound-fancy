+++++++++++++++++++++++++++++++++++++++++++++++++
Decorators Sound Way Fancier Than They Really Are
+++++++++++++++++++++++++++++++++++++++++++++++++

Talk Abstract
=============

I remember being scared of decorators.

This talk is the talk I wished somebody gave me to explain how they
work.

And I’ll throw in some stuff that I’ve learned the hard way after
misusing them.

Outline
=======

Tracing code
------------

I put logs at the top, middle and end of this function to what is going
on::

.. code-block:: python

    >>> import logging
    >>> log = logging.getLogger("dsf")
    >>> def nominal_per_capita_gross_domestic_product(
    ...     nominal_consumption,
    ...     nominal_investment,
    ...     nominal_government_spending,
    ...     nominal_net_exports,
    ...     population_count):
    ...
    ...     log.debug("C: {}".format(nominal_consumption))
    ...     log.debug("I: {}".format(nominal_investment))
    ...     log.debug("G: {}".format(nominal_government_spending))
    ...     log.debug("X: {}".format(nominal_net_exports))
    ...
    ...     nominal_Y = sum([nominal_consumption,
    ...         nominal_investment,
    ...         nominal_government_spending,
    ...         nominal_net_exports])
    ...
    ...     log.debug("Nominal GDP: {0}".format(nominal_Y))
    ...
    ...     nominal_per_capita_gdp = nominal_Y / population_count
    ...
    ...     log.debug("per-capita GDP: {0:0.2f}".format(
    ...         nominal_per_capita_gdp))
    ...
    ...     return nominal_per_capita_gdp
    ...
    >>> nominal_per_capita_gross_domestic_product(100, 110, 120, 130, 50)
    9.2


Walk through a decorator named trace that prints passed-in arguments and
the return value of a function.





Apply trace with and without the @ operator.

Study the trace source code.

Study when the decorator fires vs when when the decorated function
fires.

The property decorator lets you set getters and setters on your
instances.

Beware!  Decorators hide helpful stuff like your function’s docstring
and argument names.

The decorator package solves that problem.

Class instances can be decorators too. This lets you pass arguments to
your decorator.

You can decorate classes too.

The name “decorator” is just a python label. These are really function
closures and have been around in interpreted languages since before the
Unix epoch.

Function currying and partial function application can be done with
decorators.

Matt’s opinions and advice
==========================

Debugging decorated code SUCKS.

For all this wacky stuff, when in doubt, be verbose and redundant and
boring.  Pick "easy to debug" over "looks so cool".  Only write a
decorator AFTER you’ve pushed the boring boilerplate code to production
and you know it works.

It's helpful to debug when you can get at the undecorated version of a
function, so you should add an attribute pointing to the original
undecorated function.

Decorators should not replace argument names with ``(*args, **kwargs).``

Order of stacked decorators should not matter.

.. verify doctests like so: $ python -m doctest README.rst
.. vim: set syntax=rst:
