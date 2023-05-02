from typing import Optional
from pathlib import Path
from itertools import zip_longest
from collections import defaultdict

import click
import graphviz  # type: ignore

from .scans import trace_flow, function_list


@click.group()
def cli():
    pass


@click.command()
@click.argument('files', nargs=-1)
def list_functions(files: list[Path]):
    f_lst = function_list(files)
    print("\n".join(f_lst))


@click.command()
@click.argument('files', nargs=-1)
def global_access(files: list[Path]):
    t = trace_flow(files)
    print("assignments:", t.assignments)
    print("access:", t.access)
    print("calls:", t.calls)


@click.command()
@click.option('-o', '--output')
@click.option('-e', '--engine', default="dot")
@click.option('-r', '--root')
@click.argument('files', nargs=-1)
def graph(output: Path, engine: str, root: Optional[str], files: list[Path]):
    t = trace_flow(files)
    g = graphviz.Digraph()
    g.attr(rankdir="LR")

    write_count: defaultdict[str,int] = defaultdict(lambda: 0)
    for f in t.functions:
        for v in t.assignments[f]:
            write_count[v] += 1
    write_once = set(v for v in write_count if write_count[v] == 1)

    def add_function(f):
        consts = t.access[f].intersection(write_once)
        readonly = t.access[f] - t.assignments[f] - consts
        readwrite = t.assignments[f]
        table_rows = zip_longest(sorted(consts), sorted(readonly), sorted(readwrite))
        label = """<
        <table><tr><td colspan="3"><b>{title}</b></td></tr>
        <tr><td>const</td> <td>read-only</td> <td>modify</td></tr>
        {rows}
        </table>
        >""".format(title=f, rows="".join(
            f"<tr><td border=\"0\">{co or ''}</td><td border=\"0\">{ro or ''}</td><td border=\"0\">{rw or ''}</td></tr>"
            for co, ro, rw in table_rows))
        g.node(f, label=label, shape="plaintext")
        for e in t.calls[f]:
            g.edge(f, e)

    if root is None:
        for f in t.functions:
            add_function(f)
    else:
        assert(root in t.functions)
        visited = set()
        stack = [ root ]
        while stack:
            n = stack.pop()
            if n in visited:
                continue
            add_function(n)
            visited.add(n)
            stack.extend(t.calls[n])

    fmt = Path(output).suffix.strip('.')
    g.render(outfile=output, format=fmt, engine=engine)


cli.add_command(list_functions)
cli.add_command(global_access)
cli.add_command(graph)
cli()