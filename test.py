import thread_pool
import time


def pr(a):
    print a

#test give it a life
try:
    pool = thread_pool.ThreadPool(3)
    pool.addTask(pr, ['asdf'])
    pool.addTask(pr, ['asdf2'])
    pool.addTask(pr, ['asdf'])
    pool.addTask(pr, ['asdf'])
    time.sleep(4)
    pool.addTask(pr, ['asdf'])
    pool.addTask(pr, ['asdf2'])
    pool.addTask(pr, ['asdf'])
    pool.addTask(pr, ['asdf'])
except:
    pool.wait_and_stop_all()
