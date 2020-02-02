# Description

Identify GQ surfaces representing cylinders and replace them with ``C/X``,
``C/Y`` or ``C/Z`` surfaces with respective transformations.

The ``GQ`` surfaces are analysed. For each ``GQ`` surface satisfying criteria that it
represents a cylinder, the cylinder parameters -- its axis directoin, position
and radius -- are defined. A new cylinder surface card is added to the
surface cards block and a new transformation card is added to the data cards
block. The original ``GQ`` card is commented out and other comment lines containing
information about the precision of the computed cylinder parameters is added to 
the surface cards block.   

## Optional arguments

``-t N`` specifies the first transformation number. If not specified,
transformation numbers start from 1.

``-c`` if not ``0``, the original ``GQ`` card remains in the input, but
commented out. Otherwise, it is deleted from the input. By default, ``-c`` is
0, so that the original ``GQ`` card does not remain in the input file. 


## Rationale

An arbitrary cylinder can be represented in MCNP in via two different
techniques. One of the technique is to define a cylindrical surface in a local
coordinate system, where the cylinder is parallel to one of the axes and can be
described by ``C/X``, ``C/Y`` or ``C/Z`` surface card, and than apply a
transform. The other technique is to use the ``GQ`` card that describes a
general 4-th order surface, and in particular an arbitrary located cylinder.

Some CAD-to-MCNP converters, for example,
[McCAD](https://github.com/inr-kit/mccad.git) use the ``GQ``-based technique as it is
straighforward in programming  (knowing parameters of the cylinder one can
readily compute the parameters of the ``GQ`` card). There are however, some
drawbacks of this technique. 

One drawback is that the parameters of the ``GQ`` card are difficult to
interprete. First, it cannot be readily seen whether the ``GQ`` card represents
a cylinder or some other surface type. And when it represents a cylinders, its
parameters -- the axis direction and radius are not seen from the ``GQ``
parameters as well. 

The other drawback is related to the precision, required for the ``GQ`` card
parameters in some curcumstances (one example, a few-mm radius cylinder,
located several meters from the coordinate system origin, is discussed at the
INR seminar).  The ``GQ`` card parameters, specified in the input file with
insufficient precision can lead to geometry errors and particle losts that are
difficult to identify.


TODO: refer to the internal INR seminar discussion.


## Invocation example

```bash
>numjuggler --mode nogq2 input.orig > input.new
```
