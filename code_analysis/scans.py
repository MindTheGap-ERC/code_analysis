from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from collections import defaultdict
import re

from .mawk import on_match, run, RuleSet


@dataclass
class ListFunctions(RuleSet):
    functions: set[str] = field(default_factory=set)

    @on_match(r"function.* ([a-zA-Z_]+)\(glob,.*\)")
    def open_function(self, m):
        function_name = m[1]
        self.functions.add(function_name)


@dataclass
class TraceGlobals(RuleSet):
    functions: set[str] = field(default_factory=set)
    current_fn: Optional[str] = None
    assignments: defaultdict = field(default_factory=lambda: defaultdict(set))
    access: defaultdict = field(default_factory=lambda: defaultdict(set))
    calls: defaultdict = field(default_factory=lambda: defaultdict(list))

    @on_match(r"function.* ([a-zA-Z_]+)\(glob,.*\)")
    def open_function(self, m):
        function_name = m[1]
        self.current_fn = function_name

    @on_match(r"^[^=%]*glob\.([a-zA-Z]+)[^=<>;]*=(?!=).*")
    def glob_assign(self, m):
        if self.current_fn is None:
            return
        self.assignments[self.current_fn].add(m[1])

    @on_match(r"^.*glob\.([a-zA-Z_]+).*$")
    def glob_access(self, m):
        if self.current_fn is None:
            return

        for sub in re.findall(r"glob\.([a-zA-Z_]+)", m[0]):
            self.access[self.current_fn].add(sub)

    @on_match(r"^(?! *function).*([a-zA-Z_]+)\(.*$")
    def call_graph(self, m):
        for sub in re.findall(r"([a-zA-Z_]+)\(", m[0]):
            if sub in self.functions:
                self.calls[self.current_fn].append(sub)


def function_list(fs: list[Path]):
    l = ListFunctions()
    for f in fs:
        l.run(open(f, "r").read())
    return l.functions


def trace_flow(fs: list[Path]):
    t = TraceGlobals(functions=function_list(fs))
    for f in fs:
        t.current_fn = None
        t.run(open(f, "r").read())
    return t
