class Processor(object):
    def __init__(self, task, redis_queue):
        self._listener_id = task.node
        self._task_id = task.id
        self._redis_queue = redis_queue

    def start(self, pid):
        self._pid = pid
        self._redis_queue.start(self._task_id, self._listener_id, self._pid)

    def complete(self, result):
        self._redis_queue.complete(self._task_id, self._listener_id, self._pid, result)

    def fail(self, error):
        self._redis_queue.fail(self._task_id, self._listener_id, self._pid, error)
