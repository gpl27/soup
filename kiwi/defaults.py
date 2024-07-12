import json
import time
from kiwi.reporter import BaseReporter

NUM_THREADS = 4
EXPERIMENT_RUNS = 1

DEFAULT_SETTINGS = {
    'threads': NUM_THREADS,
    'runs':EXPERIMENT_RUNS
}

class JSONReporter(BaseReporter):
    def generate(self, results: list[dict]):
        report_id = time.time_ns()
        with open(f"report-{report_id}.json", "w") as file:
            file.write(json.dumps(results))
        

class CSVReporter(BaseReporter):
    def __init__(self):
        pass
    def generate(self, results: list[dict]):
        report_id = time.time_ns()
        with open(f"report-{report_id}.csv", 'w') as csvfile:
            pass