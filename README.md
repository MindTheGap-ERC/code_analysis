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

## Authors

__Johan Hidding__  
Netherlands eScience Center  
email: j.hidding [at] esciencecenter.nl   
Web page: [www.esciencecenter.nl/team/johan-hidding-msc/](https://www.esciencecenter.nl/team/johan-hidding-msc/)  

## Copyright

Copyright 2023 Netherlands eScience Center and Utrecht University

## License

Apache 2.0 License, see LICENSE file for license text.

## Funding information
Funded by the European Union (ERC, MindTheGap, StG project no 101041077). Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.
![European Union and European Research Council logos](https://erc.europa.eu/sites/default/files/2023-06/LOGO_ERC-FLAG_FP.png)
