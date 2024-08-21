try:
    from kiwi.kiwi import Kiwi
except ImportError:
    import sys
    sys.path.append(sys.path[0] + '/..')
    from kiwi.kiwi import Kiwi
from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS, JSONReporter
from utils import extract_results, SoupReporter

def main():
    SETTINGS = DEFAULT_SETTINGS.copy()
    SETTINGS['threads'] = 8
    SETTINGS['seed_flag'] = "-s"
    SETTINGS['seeds'] = [i+1 for i in range(5)]

    KiwiRunner = Kiwi(SETTINGS)

    r = 0.8
    b = 2.0
    m = 0.45
    g = 10

    for i in range(1, 3):
        for p in range(10,410,10):
            exp_name = f"ep{i:02d}-p{p}-r{r}-b{b}-m{m}-g{g}"
            exp = Experiment(f"python ../soup_runner.py population_size/s{exp_name}.dat ../instances/ep{i:02d}.dat -p {p} -b {b} -r {r} -m {m} -g {g}", exp_name)
            exp.attach_output_handler(extract_results)
            KiwiRunner.add_experiment(exp)


    KiwiRunner.run_all()

    KiwiRunner.gen_report(JSONReporter) # Save raw report
    KiwiRunner.gen_report(SoupReporter) # Save formatted report

if __name__ == '__main__':
    main()