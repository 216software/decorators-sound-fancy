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

Just the facts
==============

Tracing code
------------

When stuff breaks, I often put logs at the top, middle and end of a
function to what is going on, sort of like this::

    dsf.per_capita_GDP

This is when I run it::

    >>> dsf.per_capita_GDP(11, 12, 13, 14, 100)
    DEBUG:dsf:C: 11
    DEBUG:dsf:I: 12
    DEBUG:dsf:G: 13
    DEBUG:dsf:X: 14
    DEBUG:dsf:Nominal GDP: 50
    DEBUG:dsf:per-capita GDP: 0.50
    0.5

Applying those debugs to the top and bottom to lots of functions gets
tedious!  Also, more than half the text of the function is just
debugging crap.  This sucks.

Here's one way to do it differently.  First, I wrote a version of the
function without the logs::

    >>> dsf.per_capita_GDP_v2(11, 12, 13, 14, 50)
    1.0

Then I wrote this code::

    dsf.trace

Stuff to notice:

*   The trace function defines a new internal function named
    traced_function.

*   The returned value of trace is NOT the per capita GDP.  It
    is a function that calculates per-capita GDP.

*   ``*args`` and ``**kwargs`` are python tricks for packing / unpacking
    individual items to and from tuples and dictionaries.

    for a function like this::

        def f(a, b, c, d=None, e=None):
            pass

    The parameters a, b, c and will be lumped into ``args``, and d and e
    will be keys in the dictionary ``kwargs``.

Then I did this to create a new function::

    per_capita_GDP_with_debugging = trace(per_capita_GDP_v2)

Like I said earlier, this does NOT execute per_capita_GDP_v2.  It is
just a new function that will calculate per-capita GDP when given
inputs.

I think of it as sort of like cloning the original function and then
modifying the clone.

Now I run it::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)
    >>> dsf.per_capita_GDP_with_debugging(11, 12, 13, 14, 50)
    DEBUG:dsf:11
    DEBUG:dsf:12
    DEBUG:dsf:13
    DEBUG:dsf:14
    DEBUG:dsf:50
    DEBUG:dsf:result: 1.0
    1.0

It ain't exactly the same.  The individual parameter names aren't
specified, and there's no logging of the intermediate values.

However, that's nice


This trace can work on ANY function now.  Here's an example::

    dsf.hello_there

Apply trace to the hello_there function::

    >>> hello_there_with_debugging = dsf.trace(dsf.hello_there)
    >>> logging.basicConfig(level=logging.DEBUG)
    >>> hello_there_with_debugging
    <function trace_function.<locals>.traced_function at 0x7ff943d696a8>

Now run the run the function::

    >>> hello_there_with_debugging("Matt", last_name="Wilson")
    DEBUG:dsf:Matt
    DEBUG:dsf:last_name: Wilson
    hello, Matt Wilson!
    DEBUG:dsf:result: None


The `@` syntax
--------------

Python 2.2 added this syntax::

    @trace
    def f(x):
        return x * x

Which does the exact same thing as::

    f = trace(f)

The property decorator
----------------------

The property decorator lets you set getters and setters on your
instances::

    >>> matt = dsf.Person("Matt", "Wilson")
    >>> matt.display_name
    'Matt Wilson'
    >>> matt.display_name = "Matthew Wilson"
    >>> matt.first_name
    'Matthew'

Reading or writing the display_name attribute on Person runs code, and
you can do whatever you want.

Beware!  Decorating functions can hide important stuff!
-------------------------------------------------------

Beware!  Decorators hide helpful stuff like your function’s docstring
and argument names::

    >>> print(inspect.signature(dsf.hello_there))
    (first_name, middle_name=None, last_name=None)

But the decorated version has none of that helpful stuff::

    >>> inspect.signature(hello_there_with_debugging)
    <Signature (*args, **kwargs)>

All those lovely parameter names were wiped out!

The decorator package solves this problem
-----------------------------------------

How to use the decorator::

    dsf.trace2

And it does everything we want::

    >>> inspect.signature(dsf.hello_there) == inspect.signature(dsf.hello_there_with_trace2)
    True

    >>> print(inspect.getdoc(dsf.hello_there_with_trace2))
    This is the most important code I've ever written.

    It prints a string.

    >>> hello_there("stupid")
    hello, stupid!

    >>> hello_there("stupid", "and", "ugly")
    hello, stupid and ugly!

    >>> hello_there("Matt", last_name="Wilson")
    hello, Matt Wilson!

The dazzletypes example
-----------------------

Imagine you're measuring some volume in a bath tub by reading the height
of the water on the side of the tub.

If the tub is not full enough, you have to figure out the volume of
water to add, sort of like::

    if current_tub_level < ideal_level:
        current_volume = infer_volume(current_level)
        ideal_volume = infer_volume(ideal_level)
        refill(ideal_volume - current_volume):

Seems easy, but what if you stored the ideal height in the ideal volume
variable?

We wrote some code to do type-checking during comparisons, so any time
you compare a volume metric to a length metric, stuff blows up.

Think of it sort of like type-checking::

    class Milliliter(numbers.Real):

        """
        >>> Milliliter(4)
        Milliliter(4.0)

        >>> Milliliter(4000) < Millimeter(5000)
        Traceback (most recent call last):
        ...
        TypeError: Millimeter(5000) is a <class 'Millimeter'>!

        >>> Milliliter(0) >= 1
        False
        """

        @decorator.decorator
        def maybe_raise_type_error(method, self, val):

            if isinstance(val, (Milliamp, Millimeter)):
                raise TypeError("{0} is a {1}!".format(val, val.__class__))

            else:
                return method(self, val)

        @maybe_raise_type_error
        def __lt__(self, other):

            if isinstance(other, self.__class__):
                return self.val < other.val

            else:
                return self.val < other


Use a class for a decorator
---------------------------

Imagine you want to do something like this::

    @SuperTrace(log_beginning_stuff=True, log_ending_stuff=False)
    def hello_there(first_name, middle_name=None, last_name=None):

In other words, you want to tweak how your decorator works.

Here's one way to do it::

    dsf.SuperTrace

And it works like we want::

    >>> dsf.hello_there_again("Matt")
    DEBUG:dsf:In here
    DEBUG:dsf:Matt
    hello again, Matt!

On the downside, these kinds of decorators tend to obliterate the
signature.  I'm sure there's a way to use the decorator module to stop
this, but I can't find it.


These are really just function closures
---------------------------------------

The name "decorator" is just a python label. These are really function
closures and have been around in interpreted languages since before the
Unix epoch.

Function currying
-----------------

Function currying (aka partial function application) can be done with
decorators.  Currying looks sort of like this::

    >>> def add_x_and_y(x, y):
    ...     return x + y

    >>> def add_x_and_99(x):
    ...     return add_x_and_y(x, 99)

    >>> import functools
    >>> add_x_and_33 = functools.partial(add_x_and_y, y=33)
    >>> add_x_and_33(1)
    34

Essentially, you copy the function and freeze a parameter.  Mostly this
is useful in callback scenarios.

Matt’s opinions and advice
==========================

In my experience, it is very easy to mix up when the decorator defines
and returns the inner function and when the decoratored function is
called.

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

.. vim: set syntax=rst tw=72:
