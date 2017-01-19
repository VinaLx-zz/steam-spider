from math import ceil
from multiprocessing import Process
import os

if __name__ == '__main__':
    import worker
else:
    from . import worker


def start_one_worker(start, work_each, db_config):
    print('worker start, pid:{0}'.format(os.getpid()))
    w = worker.Worker((start, start + work_each), db_config)
    w.work()


class WorkerPool:
    def __init__(self, total_work, worker_num, db_config):
        self._total_work = total_work
        self._worker_num = worker_num
        self._db_config = db_config

    def start(self):
        self._init_subprocess()
        self._start_subprocess()
        self._join_subprocess()

    def _init_subprocess(self):
        self._processes = []
        work_each = ceil(self._total_work / self._worker_num)
        for start in range(1, self._total_work, work_each):
            proc = Process(
                    target=start_one_worker, args=(
                        start, work_each, self._db_config))
            self._processes.append(proc)

    def _start_subprocess(self):
        for proc in self._processes:
            proc.start()

    def _join_subprocess(self):
        for proc in self._processes:
            proc.join()

if __name__ == '__main__':
    total_work = 20
    worker_num = 2
    import json
    with open('database/db.json') as f:
        db_config = json.load(f)
    p = WorkerPool(total_work, worker_num, db_config)
    p.start()
