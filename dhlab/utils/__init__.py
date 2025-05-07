"""Utility functions."""

import importlib
import re


class LazyLoader:
    """Thin shell class to wrap modules.
    Load real module on first access and pass through.

    Code from Stackoverflow: https://stackoverflow.com/a/78312617
    """

    def __init__(me, modname):
        me._modname = modname
        me._mod = None

    def __getattr__(me, attr):
        "import module on first attribute access"

        try:
            return getattr(me._mod, attr)

        except Exception as e:
            if me._mod is None:
                # module is unset, load it
                me._mod = importlib.import_module(me._modname)
            else:
                # module is set, got different exception from getattr ().  reraise it
                raise e

        # retry getattr if module was just loaded for first time
        # call this outside exception handler in case it raises new exception
        return getattr(me._mod, attr)


def _is_documented_by(original):
    """Decorator to reuse docstrings for several functions.

    Fetch the docstring of another ``original`` function,
    and assign it as the docstring of the decorated function.

    Code copied from `StackExchange <https://softwareengineering.stackexchange.com/a/386758>`_.

    :param Callable original: Function that is decorated
    :return: The ``target`` function, with the ``original`` docstring

    **Example use:**

    .. code-block:: python

       def original(args):
           '''A complete docstring.

           :param args: Arguments.
           '''
           ...

       @_is_documented_by(original)
       def target(args):
           ...
    """

    def wrapper(target):
        target.__doc__ = original.__doc__
        return target

    return wrapper


def _docstring_parameters_from(original, drop: str | None = None):
    """Extract only parameter descriptions from ``original``'s docstring.

    Optionally, specify a ``drop`` parameter to skip in the parameter list,
    and append the rest. Can be a comma-separated string of several parameters.

    Otherwise, the wrapper works the same way as :func:`_is_documented_by`.
    """

    def _remove_param_desc(text, skip):
        regx = re.compile(rf"(\s*:param.+{skip}:\s.+\n\s *.+)(?=\n\s*:param)")
        skip_str = re.search(regx, text).group()
        return text.replace(skip_str, "")

    def wrapper(target):
        docstr = original.__doc__
        parameters = docstr[docstr.index("\n\n    :param") :]
        if drop is not None:
            for skip in drop.split(","):
                parameters = _remove_param_desc(parameters, skip)
        target.__doc__ += "\n" + parameters
        return target

    return wrapper
