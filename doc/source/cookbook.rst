.. _operation:

|NAME| cookbook
===============

A pipeline algorithm is implemented using classes from the :mod:`cmpipe` module.
The building blocks of pipelines map to specific Python objects:

 +---------------------+-------------------------------------+
 |  Framework element  |  Python construct                   |
 +=====================+=====================================+
 |  *task*, *result*   |  any Python picklable object        |
 +---------------------+-------------------------------------+
 |  *worker*           |  single-argument function,          |
 |                     |  :mod:`~cmpipe.OrderedWorker` or     |
 |                     |  :mod:`~cmpipe.UnorderedWorker`      |
 +---------------------+-------------------------------------+
 |  *stage*            |  :mod:`~cmpipe.Stage`,               |
 |                     |  :mod:`~cmpipe.OrderedStage` or      |
 |                     |  :mod:`~cmpipe.UnorderedStage`       |
 +---------------------+-------------------------------------+
 |  *pipeline*         |  :mod:`~cmpipe.Pipeline`             |
 +---------------------+-------------------------------------+

It may be useful to keep in mind that |NAME| is built using classes from Python's standard :mod:`multiprocessing` module. It is a layer on top, encapsulating classes like :class:`~multiprocessing.Process`, :class:`~multiprocessing.Queue` and :class:`~multiprocessing.Connection` with behavior specific to the pipeline workflow.

The procedure of building and running a pipeline is a sequence of five steps:

  #. :ref:`define workers <define_workers>`
  #. :ref:`create stage objects <create_stage_objects>`
  #. :ref:`link the stages <link_the_stages>`
  #. :ref:`create pipeline object <create_pipeline_object>`
  #. :ref:`operate the pipeline <operate_the_pipeline>`

.. _define_workers:

1. Define workers
-----------------

Start by defining the work that will be performed by individual workers of your stages. The easiest way is to write a function that takes a single *task* parameter:
::

  def doSomething(task):
     result = f(task)
     return result

The function's return value becomes result of the stage. If it doesn't return anything (or ``None``), then the stage is considered a dead-end stage, not producing any output.

The other way is to subclass from :mod:`~cmpipe.OrderedWorker` or :mod:`~cmpipe.UnorderedWorker` and put the actual work inside the :meth:`doTask()` method:
::

  class MyWorker(cmpipe.OrderedWorker):
     def doTask(task):
        result = f(task)
        return result

Just like when using a standalone function, stage result is the return value of :meth:`doTask()`. Another option is to call :meth:`putResult()`. This can be useful if you want your worker to continue processing after registering the stage result:
::

  class MyWorker(cmpipe.OrderedWorker):
     def doTask(task):
        result = f(task)
        self.putResult(result)
        # Do some more stuff.

.. _create_stage_objects:

2. Create stage objects
-----------------------

Having defined your workers, the next step is to instantiate stage objects. With standalone work functions, the stage is created with :mod:`~cmpipe.OrderedStage` or :mod:`~cmpipe.UnorderedStage`.
::
  
  stage1 = cmpipe.OrderedStage(doSomething, 3)

When using worker classes, create a :mod:`~cmpipe.Stage` object instead:
::

  stage2 = cmpipe.Stage(MyWorker, 4)

In both cases the second argument is the number of processes devoted to the particular stage. 

.. _link_the_stages:

3. Link the stages
------------------

If there are multiple stages in the workflow, they can be linked together in series:
::

  stage1.link(stage2)
  stage2.link(stage3)

The :meth:`~cmpipe.Stage.link` method returns the stage object it is called on, allowing you to serially link many stages in a single statement. Here's the equivalent of above:
::

  stage1.link(stage2.link(stage3))

Output of one stage may also be forked into multiple downstream stages, splitting the workflow into parallel streams of execution:
::

  stage1.link(stage2)
  stage1.link(stage3)
  stage1.link(stage4)


.. _create_pipeline_object:

4. Create pipeline object
-------------------------

A pipeline is created by passing the root upstream stage to the :mod:`~cmpipe.Pipeline` constructor:
::

  pipe = cmpipe(stage1)

Once built, the pipeline has allocated and started all designated processes. At this point the pipeline is waiting for input, its worker processes idle and ready.

.. _operate_the_pipeline:

5. Operate the pipeline
-----------------------

From this point on, operating the pipeline is solely accomplished by manipulating the :mod:`~cmpipe.Pipeline` object. Input tasks are fed using :meth:`~cmpipe.Pipeline.put()`:
::

  pipe.put(something)

Output results, if any, are fetched using :meth:`~cmpipe.Pipeline.get()`:
::

  result = pipe.get()

Alternatively, one can iterate the output stream with :meth:`~cmpipe.Pipeline.results()` method:
::

  for result in pipe.results():
     print(result)

At some point in manipulating the pipeline, the special task ``None`` should be put on it.
::

  pipe.put(None)

This signals the end of input stream and eventually terminates all worker processes, effectively "closing" the pipeline to further input. 

The ``None`` task can be thought of as a "stop" request. It becomes part of the sequence of input tasks streaming into the pipeline and, like other tasks, it propagates through all stages. However, it is processed in a special way: when it arrives at a stage, it signals all worker processes within to complete any current task they may be running, and to terminate execution. Before the last worker terminates, it propagates the "stop" request to the next downstram stage (or stages, if forked).

The ``None`` task should be the last input to the pipeline. After it is added to the stream of tasks, the pipeline continues to process any previous tasks still in the system. After worker processes terminate, results can still be accesses in the usual way (using :meth:`~cmpipe.Pipeline.get()` or :meth:`~cmpipe.Pipeline.results()`) until the pipeline is emptied. However, any "real" task (i.e. not ``None``) put on the pipeline following the "stop" request will not be processed.
