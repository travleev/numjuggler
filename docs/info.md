# Description 
The input file is analysed and ranges of used numbers for cells, surfaces,
ets. are written to the standard output. Note that the output of this mode can
be used (after necessary modifications) as the input to the `--map` option.

The first two columns specify type (cells, surfaces, etc.) and the range of
used numbers. The third column shows the amount of numbers in current range,
and the last column shows how many numbers left unused between the current and
previous ranges.

# Invocation example

The input file `input.orig` is analysed and the result is redirected to `info.txt`:

    >numjuggler --mode info input.orig > info.txt
    
    
