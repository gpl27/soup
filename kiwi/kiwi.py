from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS
from kiwi.reporter import BaseReporter
from multiprocessing import Pool

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
        self._experiments: list[Experiment] = []

    @classmethod
    def load(path: str):
        pass

    def run_all(self):
        with Pool(self._settings["threads"]) as pool:
            results = pool.map(self.run, self._experiments)
            for exp, r in zip(self._experiments, results):
                exp._runs += r
            pool.close()
            pool.join()

    def run(self, experiment: Experiment):
        """TODO: Is `experiment` a random experiment, or one of the
        experiments in `self._experiments`"""
        seeds = self._settings.get("seeds")
        runs = []
        if seeds:
            for seed in seeds:
                runs.append(experiment.run(f" --SEED {seed}"))
        else:
            for i in range(self._settings["runs"]):
                runs.append(experiment.run())
        return runs

    def add_experiment(self, experiment: Experiment):
        self._experiments.append(experiment)

    def gen_report(self, reporter: BaseReporter):
        results = [exp.get_results() for exp in self._experiments]
        reporter.generate(results)

