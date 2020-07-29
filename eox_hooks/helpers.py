"""Module to define convenient utilities."""
import time


class Timer(object):
    """Class used for timing tasks execution."""
    def __init__(self, timing=False):
        """
        Init method.

        Arguments:
            - timing: indicates if the timer is going to be used. This is useful when
            using or not the timer depends on a configuration.
        """
        self._start_time = None
        self.timing = timing

    def start(self):
        """Function that starts a new timer."""
        if self.timing:
            self._start_time = time.time()

    def stop(self):
        """Function that stops the timer, and report the elapsed time."""
        if self.timing:
            elapsed_time = time.time() - self._start_time

        return elapsed_time
