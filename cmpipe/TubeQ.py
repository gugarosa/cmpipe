"""Implements TubeQ class."""

import multiprocessing

class TubeQ:
    """A unidirectional communication channel 
    using :class:`multiprocessing.Queue` for underlying implementation."""

    def __init__(self, maxsize=0, process_start_method='spawn'):
        self._default_start_method = multiprocessing.get_start_method()
        multiprocessing.set_start_method(process_start_method, True)
        self._queue = multiprocessing.Queue(maxsize)
        multiprocessing.set_start_method(self._default_start_method, True)

    def put(self, data):
        """Put an item on the tube."""
        self._queue.put(data)

    def get(self, timeout=None):
        """Return the next available item from the tube.

        Blocks if tube is empty, until a producer for the tube puts an item on it."""
        if timeout:
            try:
                result = self._queue.get(True, timeout)
            except multiprocessing.Queue.Empty:
                return(False, None)
            return(True, result)
        return self._queue.get()
