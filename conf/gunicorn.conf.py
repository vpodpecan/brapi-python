import multiprocessing

bind = "127.0.0.1:8002"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 300
worker_class = 'gevent'

# raw_env = {}
