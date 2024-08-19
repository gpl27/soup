from kiwi.kiwi import Kiwi
from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS, JSONReporter

SETTINGS = DEFAULT_SETTINGS.copy()
SETTINGS['threads'] = 8
SETTINGS['seeds'] = [i+1 for i in range(5)] # Run each experiment 5 times with diff seeds

# Initialize runner with settings
KiwiRunner = Kiwi(SETTINGS)

# Create an output handler
def extract_results(run_info: dict, byte_array: bytes):
    output = byte_array.decode()
    for line in output.splitlines():
        if "solution_value" in line:
            run_info['@solution_value'] = int(line.split(':')[1].strip())
        elif "solution_cost" in line:
            run_info['@solution_cost'] = int(line.split(':')[1].strip())
        elif "non_improving_generations" in line:
            run_info['@non_improving_generations'] = int(line.split(':')[1].strip())
        elif "generations" in line:
            run_info['@generations'] = int(line.split(':')[1].strip())
        elif "seed" in line:
            run_info['@seed'] = int(line.split(':')[1].strip())
        elif "runtime" in line:
            run_info['@runtime'] = float(line.split(':')[1].strip())

# Quickly create experiments with varying parameters
for i in range(1, 11):
    for p in [50, 100, 200, 400, 800]:
        for r in [0.2, 0.4, 0.6, 0.8, 1.0]:
            for m in [0.2, 0.4, 0.6, 0.8, 1.0]:
                exp = Experiment(f"python ./soup_runner.py ./instances/ep{i:02d}.dat -p {p} -r {r} -m {m} -t 30", f"ep{i:02d}-p{p}-r{r}-m{m}")
                exp.attach_output_handler(extract_results)
                KiwiRunner.add_experiment(exp)

# Let Kiwi take care of running them in parallel
KiwiRunner.run_all()

# See the generated report in your files
KiwiRunner.gen_report(JSONReporter)

