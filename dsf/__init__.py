# vim: set expandtab ts=4 sw=4 filetype=python fileencoding=utf8:

# Run doctests like so: $ python -m doctest dsf/__init__.py

import logging

import decorator

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("dsf")

def per_capita_GDP(
    consumption,
    investment,
    government_spending,
    net_exports,
    population_count):

    """
    Calculates the per-capita GDP for a single year, using summation
    method.

    >>> per_capita_GDP(11, 12, 13, 14, 100)
    0.5
    """

    log.debug("C: {}".format(consumption))
    log.debug("I: {}".format(investment))
    log.debug("G: {}".format(government_spending))
    log.debug("X: {}".format(net_exports))

    Y = sum([
        consumption,
        investment,
        government_spending,
        net_exports])

    log.debug("GDP: {0}".format(Y))

    per_capita_gdp = Y / population_count

    log.debug("per-capita GDP: {0:0.2f}".format(
        per_capita_gdp))

    return per_capita_gdp

def trace(f):

    def traced_function(*args, **kwargs):

        for arg in args:
            log.debug(arg)

        for k, v in kwargs.items():
            log.debug("{0}: {1}".format(k, v))

        result = f(*args, **kwargs)

        log.debug("result: {0}".format(result))

        return result

    return traced_function

def per_capita_GDP_v2(
    consumption,
    investment,
    government_spending,
    net_exports,
    population_count):

    """
    Calculates the per-capita GDP for a single year, using summation
    method.

    >>> per_capita_GDP(11, 12, 13, 14, 100)
    0.5
    """

    Y = sum([
        consumption,
        investment,
        government_spending,
        net_exports])

    per_capita_gdp = Y / population_count

    return per_capita_gdp

per_capita_GDP_with_debugging = trace(per_capita_GDP_v2)

def hello_there(first_name, middle_name=None, last_name=None):

    """
    This is the most important code I've ever written.

    It prints a string.

    >>> hello_there("stupid")
    hello, stupid!

    >>> hello_there("stupid", "and", "ugly")
    hello, stupid and ugly!

    >>> hello_there("Matt", last_name="Wilson")
    hello, Matt Wilson!

    """

    display_name = first_name

    if middle_name:
        display_name = "{0} {1}".format(display_name, middle_name)

    if last_name:
        display_name = "{0} {1}".format(display_name, last_name)

    print("hello, {0}!".format(display_name))

class Person(object):

    def __init__(self, first_name, last_name):

        self.first_name = first_name
        self.last_name = last_name

    @property
    def display_name(self):
        return "{0} {1}".format(
            self.first_name,
            self.last_name)

    @display_name.setter
    def display_name(self, val):

        a, b = val.split(" ", 2)

        if a.strip() and b.strip():
            self.first_name = a
            self.last_name = b

        else:
            raise ValueError("Huh?!?! {0}".format(val))

@decorator.decorator
def trace2(f):

    def traced_function(*args, **kwargs):

        for arg in args:
            log.debug(arg)

        for k, v in kwargs.items():
            log.debug("{0}: {1}".format(k, v))

        result = f(*args, **kwargs)

        log.debug("result: {0}".format(result))

        return result

    return traced_function

hello_there_with_trace2 = trace2(hello_there)

class SuperTrace(object):

    def __init__(self, log_beginning_stuff=True, log_ending_stuff=True):

        self.log_ending_stuff = log_ending_stuff
        self.log_beginning_stuff = log_beginning_stuff

    def __call__(self, f):

        def traced_f(*args, **kwargs):

            log.debug("In here")

            if self.log_beginning_stuff:

                for arg in args:
                    log.debug(arg)

                for k, v in kwargs.items():
                    log.debug("{0}: {1}".format(k, v))

            result = f(*args, **kwargs)

            if self.log_ending_stuff:
                log.debug("result: {0}".format(result))

            return result

        return traced_f

@SuperTrace(log_beginning_stuff=True, log_ending_stuff=False)
def hello_there_again(first_name, middle_name=None, last_name=None):

    """
    This is the most important code I've ever written.

    It prints a string.

    >>> hello_there_again("stupid")
    hello again, stupid!

    >>> hello_there_again("stupid", "and", "ugly")
    hello again, stupid and ugly!

    >>> hello_there_again("Matt", last_name="Wilson")
    hello again, Matt Wilson!

    """

    display_name = first_name

    if middle_name:
        display_name = "{0} {1}".format(display_name, middle_name)

    if last_name:
        display_name = "{0} {1}".format(display_name, last_name)

    print("hello again, {0}!".format(display_name))
