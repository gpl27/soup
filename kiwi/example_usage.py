from kiwi.kiwi import Kiwi
from kiwi.experiment import Experiment
from kiwi.defaults import DEFAULT_SETTINGS, CSVReporter

SETTINGS = DEFAULT_SETTINGS.copy()
# Run each experiment 5 times
SETTINGS['runs'] = 5

# Initialize runner with settings
KiwiRunner = Kiwi(SETTINGS)

# Quickly create experiments with varying parameters
for i in range(50, 501, 50):
    for j in range(0.1, 0.6, 0.1):
        exp = Experiment("./soup.py", f"-i ep03.dat -p {i} -s {j}", f"ep003-p{i}-s{j}")
        KiwiRunner.add_experiment(exp)

# Let Kiwi take care of running them in parallel
KiwiRunner.run_all()

# Create a custom reporter, or just use one of the defaults
Reporter = CSVReporter()

# See the generated report in your files
KiwiRunner.gen_report(Reporter)
