import thread_pool


def pr(a):
    print a

#test give it a life
pool = thread_pool.ThreadPool(3)
pool.addTask(pr, ['asdf'])
pool.addTask(pr, ['asdf2'])
pool.addTask(pr, ['asdf'])
pool.addTask(pr, ['asdf'])
pool.wait_and_stop_all()
