from __future__ import absolute_import, unicode_literals

try:
    import threading
except ImportError:
    threading = None


class ThreadCollector(object):
    def __init__(self):
        if threading is None:
            raise NotImplementedError(
                "threading module is not available, "
                "this panel cannot be used without it")
        self.collections = {}  # a dictionary that maps threads to collections

    def get_collection(self, thread=None):
        """
        Returns a list of collected items for the provided thread, of if none
        is provided, returns a list for the current thread.
        """
        if thread is None:
            thread = threading.currentThread()
        if thread not in self.collections:
            self.collections[thread] = []
        return self.collections[thread]

    def clear_collection(self, thread=None):
        if thread is None:
            thread = threading.currentThread()
        if thread in self.collections:
            del self.collections[thread]

    def collect(self, item, thread=None):
        self.get_collection(thread).append(item)
