.. _index:

.. toctree::
   :hidden:

   docs
   download
   concepts
   cookbook
   examples
   fordevelopers
   api
   about

|NAME| is a tiny Python module -- a thin layer above the standard :mod:`multiprocessing` package -- that lets you write parallel, multi-stage pipeline algorithms with remarkable ease. Consider the following workflow:

.. image:: tiny.png
   :align: center

It's a two-stage pipeline that increments and doubles numbers, each stage concurrently running three workers.
Here's how you'd code it up using the :mod:`cmpipe` module:

.. literalinclude:: tiny.py

The above snippet runs a total of seven processes: one for the main program and six for the two stages (three processes per stage).

Installation
************

Get |NAME| now! Easiest way is using *pip*:
::

  pip install cmpipe

Check out :doc:`download` for other ways of getting |NAME| up and running on your system. 

Got it, now what?
*****************

Start piping right away by running through the :doc:`examples`.
If you want a step-by-step guide to creating pipelines, read the :doc:`cookbook`.
For theory and design, take a look at :doc:`concepts`.
