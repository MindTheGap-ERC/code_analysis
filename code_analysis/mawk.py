"""
μAwk, a tiny awk-like interface in Python
"""

from typing import Callable, Optional
from functools import wraps, partial
import re


def match_filter(expr: str, handler: Callable[[re.Match], Optional[list[str]]], inp: str) -> list[str]:
    if m := re.match(expr, inp):
        result = handler(m)
        if result is None:
            return [inp]
        else:
            return result
    else:
        return [inp]


def on_match(expr: str):
    """Decorator for doing search-and-replace based on a given regex.
    
    The inner function should take as argument a `re.Match` object
    and return a list of strings. The resulting decorated function
    then becomes a function from string to list of strings.
    
    If the input doesn't match the given regex, the original string
    is returned.
    
    The inner function may still decide to do nothing by returning None.
    
    To erase the matched input return the empty list.

    This decorator also works on class methods. It is then assumed that
    the method has signature `(self, m: re.Match)`.
    """
    def _decorator(f):
        method = len(f.__qualname__.split('.')) > 1
        if method:
            @wraps(f)
            def _impl(self, inp):
                return match_filter(expr, partial(f, self), inp)
            _impl._is_rule = True  # add tag to method
            return _impl
        else:
            return wraps(f)(partial(match_filter, expr, f))
    return _decorator


Rule = Callable[[str], list[str]]


def run(rules: list[Rule], inp: str) -> str:
    """Takes a list of rules, being function from `str` to `list[str]`.
    The input string is split into lines, after which each line is fed
    through the list of rules. All the results are colected into a list
    of strings and then joined by newline.
    """
    lines = inp.splitlines()
    result = []
    for l in lines:
        for r in rules:
            result.extend(r(l))
    return "\n".join(result)


class RuleSet:
    """To be used as a base class for classes that contain `on_match`
    decorated methods."""
    def run(self, inp: str) -> str:
        """Runs all rules in the class on input."""
        members = (getattr(self, m) for m in dir(self) if m[0] != '_')
        rules = [m for m in members if hasattr(m, '_is_rule')]
        return run(rules, inp)
