import concurrent.futures
import sys

def run_app():
    from src import view
executor = concurrent.futures.ThreadPoolExecutor()
executor.submit(run_app)
