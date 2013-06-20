import os
import random
import sys
import threading
import time


class ForkingRunner(threading.Thread):
    def __init__(self, client, queue, task_callback):
        super(ForkingRunner, self).__init__()

        self._client = client
        self._queue = queue
        self._task_callback = task_callback

        self.running = threading.Event()

    def fork_task(self, task):
        pid = os.fork()

        if pid > 0:
            return pid

        # Reseed the random number generator, since we inherited it
        # from our parent after the fork
        random.seed()

        os.setsid()

        processor = self._client.get_processor(task)

        processor.start(os.getpid())

        try:
            result = self._task_callback(task)

            processor.complete(result)
        except Exception as e:
            processor.fail(str(e))
        finally:
            # _exit won't flush, so we need to, in case there are
            # error messages we want to see.
            sys.stdout.flush()
            sys.stderr.flush()

            os._exit(0)

    def run(self):
        self.running.set()

        listener = self._client.get_listener(self._queue)

        while True:
            task = listener.listen()

            pid = self.fork_task(task)

            _, status = os.waitpid(pid, 0)


def run(client, queue, task_callback, concurrency=1):
    threads = []

    while True:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < concurrency:
            thread = ForkingRunner(client, queue, task_callback)
            thread.start()

            thread.running.wait()

            threads.append(thread)

        time.sleep(1)
