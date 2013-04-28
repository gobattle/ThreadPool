import threading
import Queue
import time
import json


class ThreadWorker(threading.Thread):
    LIFE_SPAN = 30  # in second

    def __init__(self, task_queue, task_set):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.task_set = task_set
        self._is_running = False
        self._is_alive = True
        self._wait_to_kill = False
        self.born_at = time.time()

    def run(self):
        while self.check_alive():
            self.is_running = False
            try:
                callback, args_json = self.task_queue.get(timeout=0.1)
                args = json.loads(args_json)
                self.is_running = True
                try:
                    callback(*args)
                except Exception, e:
                    #TODO track exception
                    print  e
                self.task_set.remove((callback, args_json))
            except Exception, e:
                pass
            # will be kill when queue is empty
            if self._wait_to_kill and not self.is_running:
                self._is_alive = False

    def stop(self):
        self._is_alive = False

    def is_alive(self):
        return self._is_alive

    def check_alive(self):
        self._is_alive = self.is_alive() \
            and time.time() - self.born_at < self.LIFE_SPAN
        return self._is_alive

    def wait_and_stop(self):
        self._wait_to_kill = True


class ThreadPool:
    MAX_POOL_SIZE = 256
    MAX_LOAD = 4

    def __init__(self, pool_size=MAX_POOL_SIZE):
        self.pool_size = pool_size
        self.thread_list = []
        self.task_queue = Queue.Queue(self.MAX_POOL_SIZE * self.MAX_LOAD)
        self.task_set = set()
        self._initThreads()

    def _initThreads(self):
        for i in range(0, self.pool_size):
            thr = ThreadWorker(self.task_queue, self.task_set)
            self.thread_list.append(thr)
        for thr in self.thread_list:
            thr.start()

    def _removeDeadThreads(self):
        for thr in self.thread_list:
            if not thr.is_alive():
                self.thread_list.remove(thr)
                del thr

    def delThreads(self, num):
        if self.thread_list == []:
            return
        for thr in self.thread_list:
            if num > 0:
                thr.stop()
                num -= 1
        self._removeDeadThreads()

    def regain_threads(self):
        missing_num = self.pool_size - self.count_threads()
        for cpt in range(missing_num):
            thr = ThreadWorker(self.task_queue, self.task_set)
            thr.start()
            self.thread_list.append(thr)

    def stop_all(self):
        for thr in self.thread_list:
            thr._is_alive = False

    def wait_and_stop_all(self):
        for thr in self.thread_list:
            thr.wait_and_stop()

    def count_threads(self):
        self._removeDeadThreads()
        return len(self.thread_list)

    def addTask(self, callback, args):
        args_json = json.dumps(args)
        if (callback, args_json) not in self.task_set:
            self.task_queue.put((callback, args_json))
            self.task_set.add((callback, args_json))
        self.regain_threads()

    @property
    def queue_size(self):
        return self.task_queue.qsize()
