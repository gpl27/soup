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
    SETTINGS['seeds'] = [i+1 for i in range(5)] # Run each experiment 5 times with diff seeds

    KiwiRunner = Kiwi(SETTINGS)

    p = 50
    b = 2.0
    r = 0.0
    ng = 10
    t = 60*60

    for i in range(1, 3):
        for _ in range(1, 41):
            m = _/40
            exp_name = f"ep{i:02d}-p{p}-r{r}-b{b}-m{m}-ng{ng}"
            exp = Experiment(f"python ../soup_runner.py mutation_rate/s{exp_name}.dat ../instances/ep{i:02d}.dat -p {p} -b {b} -r {r} -m {m} -ng {ng} --seq -t {t}", exp_name)
            exp.attach_output_handler(extract_results)
            KiwiRunner.add_experiment(exp)


    KiwiRunner.run_all()

    KiwiRunner.gen_report(JSONReporter) # Save raw report
    KiwiRunner.gen_report(SoupReporter) # Save formatted report

if __name__ == '__main__':
    main()