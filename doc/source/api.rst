.. _api:

**********
|NAME| API
**********

.. module:: cmpipe

.. autoclass:: cmpipe.OrderedWorker
   :members: doTask, doInit, putResult

.. autoclass:: cmpipe.UnorderedWorker
   :members: doTask, doInit, putResult

----

.. autoclass:: cmpipe.Stage
   :members: link, put, get

.. autoclass:: cmpipe.OrderedStage
   :members:

.. autoclass:: cmpipe.UnorderedStage
   :members:

----

.. autoclass:: cmpipe.Pipeline
   :members: put, get, results

----

.. autoclass:: cmpipe.FilterWorker

.. autoclass:: cmpipe.FilterStage

.. End of file.
