===================================
Hypothesis for the Scientific Stack
===================================

.. _hypothesis-numpy:

-----
numpy
-----

Hypothesis offers a number of strategies for `NumPy <http://www.numpy.org/>`_ testing,
available in the :mod:`hypothesis[numpy]` :doc:`extra </extras>`.
It lives in the ``hypothesis.extra.numpy`` package.

The centerpiece is the :func:`~hypothesis.extra.numpy.arrays` strategy, which generates arrays with
any dtype, shape, and contents you can specify or give a strategy for.
To make this as useful as possible, strategies are provided to generate array
shapes and generate all kinds of fixed-size or compound dtypes.


.. automodule:: hypothesis.extra.numpy
   :members:
