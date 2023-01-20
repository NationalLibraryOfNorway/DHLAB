"""Utility functions."""
import re


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


def _docstring_parameters_from(original, drop: str = None):
    """Extract only parameter descriptions from ``original``'s docstring.

    Optionally, specify a ``drop`` parameter to skip in the parameter list,
    and append the rest. Can be a comma-separated string of several parameters.

    Otherwise, the wrapper works the same way as :func:`_is_documented_by`.
    """

    def _remove_param_desc(text, skip):
        regx = re.compile(fr'(\s*:param.+{skip}:\s.+\n\s *.+)(?=\n\s*:param)')
        skip_str = re.search(regx, text).group()
        return text.replace(skip_str, "")

    def wrapper(target):
        docstr = original.__doc__
        parameters = docstr[docstr.index("\n\n    :param"):]
        if drop is not None:
            for skip in drop.split(","):
                parameters = _remove_param_desc(parameters, skip)
        target.__doc__ += "\n" + parameters
        return target
    return wrapper
