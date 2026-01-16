# Measure time spent in each pipeline stage.
#backend/app/utils/observability/metrics.py
#Measure execution time of a code block without cluttering logic.
import time
from contextlib import contextmanager

@contextmanager
def track_latency(metrics: dict, key:str):
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    metrics[key] = end-start




