"""Implements Pipeline class."""
import multiprocessing

class Pipeline(object):
    """A pipeline of stages."""
    def __init__(self, input_stage, process_start_method='spawn'):
        """Constructor takes the root upstream stage."""
        self._input_stage = input_stage
        self._output_stages = input_stage.getLeaves()
        self._default_start_method = multiprocessing.get_start_method()
        multiprocessing.set_start_method(process_start_method, True)
        self._input_stage.build()
        multiprocessing.set_start_method(self._default_start_method, True)

    def put(self, task):
        """Put *task* on the pipeline."""
        self._input_stage.put(task)

    def get(self, timeout=None):
        """Return result from the pipeline."""
        result = None
        for stage in self._output_stages:
            result = stage.get(timeout)
        return result

    def results(self):
        """Return a generator to iterate over results from the pipeline."""
        while True:
            result = self.get()
            if result is None: break
            yield result

    def shutdown(self):
        self._input_stage.join()
