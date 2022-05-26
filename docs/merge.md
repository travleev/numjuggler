# Description 
The `merge` mode puts two separate input files into a single input file.
One input file is specified as the positional command line argument, the other
input file is specified as the argument to `-m`. 
The example invocation:

    >numjuggler --mode merge -m inp2.inp inp1.inp > merged.inp

The resulting input file in this example written into `merged.inp`. It
contains cell, surface and data blocks from `inp1.inp` and `inp2.inp`. The
title of the merged input is taken from `inp1.inp` if it exists, otherwise from
`inp2.inp`. In each block first the cards from `inp1.inp` are written; they are
followed by the cards from `inp2.inp`.

Note: this mode only places content of two input files in proper order, i.e.
cells, surfaces and data cards to the respective blocks. The cell, surface and
other numbers are not changed. To ensure that the models to be merged have
unique names for cell, surfaces, etc., they should be modified before merging. 

