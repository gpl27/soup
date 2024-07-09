from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS

class Kiwi:
    """Kiwi is configurable program runner.
    By default, Kiwi will time the program runs and run
    them in parallel. You can also configure
    how to treat the programs output, where you can
    add custom properties to the Kiwi object, that
    will become part of your results
    TODO:
        * Define how reports will work
        * What happens when you run .run_all() more than once
        * How to save things? For now can just pickle Kiwi object,
        but should consider just saving results, and settings as JSON
    """
    def __init__(self, settings: dict =DEFAULT_SETTINGS):
        self._settings = settings

    @classmethod
    def load(path: str):
        pass

    def run_all(self):
        pass

    def run(self, experiment: Experiment):
        pass

    def add_experiment(self, experiment: Experiment):
        pass

    def gen_report(self, reporter):
        pass

