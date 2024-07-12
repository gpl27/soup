import os
from kiwi.kiwi import Kiwi
from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS, JSONReporter

SETTINGS = DEFAULT_SETTINGS.copy()
# Run each experiment 5 times
SETTINGS['runs'] = 5

# Initialize runner with settings
KiwiRunner = Kiwi(SETTINGS)

# Create an output handler
def extract_important(run_info: dict, byte_array: bytes):
    output = byte_array.decode()
    for line in output.splitlines():
        if "IMPORTANT" in line:
            run_info['@code'] = line.split(':')[1]

# Quickly create experiments with varying parameters
filename = os.path.abspath("./kiwi_example_script.sh")
for i in range(50, 501, 50):
    for j in [x / 10.0 for x in range(1, 6, 1)]:
        exp = Experiment(f"{filename} {i*j}", f"exp-{i}-{j}")
        exp.attach_output_handler(extract_important)
        KiwiRunner.add_experiment(exp)

# Let Kiwi take care of running them in parallel
KiwiRunner.run_all()

# Create a custom reporter, or just use one of the defaults
Reporter = JSONReporter()

# See the generated report in your files
KiwiRunner.gen_report(Reporter)
