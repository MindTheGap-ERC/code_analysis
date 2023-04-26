# Matlab Code analysis tool
This tool reads Matlab code and creates an overview of a callgraph, showing for each function what constants are being read, what mutable variables and what variables are being written to. The reason it can do this is because the code I'm trying to analyse has a quite rigid structure for dealing with global variables.

Each function involved has the following shape:

```matlab
function [glob] = MyFunction(glob, other_args)
    ...
end
```

This script requires Python with the `click` and `graphviz` modules installed (or run `pip install .` inside your favourite VirtualEnv).

To create the call graph in a place where all your Matlab code lives, run:

```sh
code_analysis graph -o callgraph.pdf *.m
```

