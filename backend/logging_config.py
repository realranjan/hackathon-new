import logging
import logging.handlers
import os
import sys
import json

def setup_logging():
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'supplywhiz.log')
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    formatter = logging.Formatter(json.dumps({
        'time': '%(asctime)s',
        'level': '%(levelname)s',
        'module': '%(module)s',
        'funcName': '%(funcName)s',
        'lineno': '%(lineno)d',
        'message': '%(message)s'
    }))
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    # Also log to stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    root.addHandler(stream_handler) 