from kiwi.reporter import BaseReporter

NUM_THREADS = 4
EXPERIMENT_RUNS = 1

DEFAULT_SETTINGS = {
    'threads': NUM_THREADS,
    'runs':EXPERIMENT_RUNS
}

class JSONReporter(BaseReporter):
    def __init__(self):
        pass

class CSVReporter(BaseReporter):
    def __init__(self):
        pass