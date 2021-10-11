import multiprocessing

name = 'Troy'
bind = 'unix:/app/Troy.sock'
workers = multiprocessing.cpu_count() * 2 + 1
keepalive = 32
worker_connections = 1000 * workers
worker_class = "gevent"
reload = True
loglevel = 'info'
logfile = '-'
spew = False

max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 15
timeout = 15

BASE_DIR = "/app/"
pythonpath = BASE_DIR
chdir = BASE_DIR

preload_app = False