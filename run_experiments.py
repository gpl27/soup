import os
from kiwi.kiwi import Kiwi
from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS, JSONReporter

SETTINGS = DEFAULT_SETTINGS.copy()
# Run each experiment 5 times
SETTINGS['threads'] = 8
SETTINGS['seeds'] = [i+1 for i in range(5)]

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
for i in range(50, 501, 50):
    for j in [x / 10.0 for x in range(1, 6, 1)]:
        exp = Experiment(f"python ./soup_runner.py ./instances/ep01.dat -p {i} -m {j} -t 5", f"exp-{i}-{j}")
        exp.attach_output_handler(extract_results)
        KiwiRunner.add_experiment(exp)

# Let Kiwi take care of running them in parallel
KiwiRunner.run_all()

# Create a custom reporter, or just use one of the defaults
Reporter = JSONReporter()

# See the generated report in your files
KiwiRunner.gen_report(Reporter)

