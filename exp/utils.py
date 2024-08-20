import json
import time
from kiwi.reporter import BaseReporter
import re

BKVs = {
    "ep01.dat": 2118,
    "ep02.dat": 1378,
    "ep03.dat": 2850,
    "ep04.dat": 2730,
    "ep05.dat": 2624,
    "ep06.dat": 4690,
    "ep07.dat": 4440,
    "ep08.dat": 5020,
    "ep09.dat": 4568,
    "ep10.dat": 4390,
}

def parse_cmd(cmd: str) -> dict:
    pcmd = dict()
    acmd = cmd.split(" ")
    pcmd["@instance"] = acmd[3].split("/")[-1]
    pcmd["@output_file"] = acmd[2]
    pcmd["@population_size"] = acmd[acmd.index("-p") + 1]
    pcmd["@recombination_rate"] = acmd[acmd.index("-r") + 1]
    pcmd["@mutation_rate"] = acmd[acmd.index("-m") + 1]
    pcmd["@beta_rank"] = acmd[acmd.index("-b") + 1]
    # pcmd["@generations"] = acmd[acmd.index("-g") + 1]
    # pcmd["@max_non_improving_generations"] = acmd[acmd.index("-ng") + 1]
    return pcmd

class SoupReporter(BaseReporter):
    @staticmethod
    def generate(results: list[dict]):
        report_id = time.time_ns()
        report = []
        for exp_result in results:
            result = dict()
            result |= parse_cmd(exp_result["cmd"])
            best_run = max(exp_result["_runs"], key=lambda r: r["@solution_value"])
            result["@best_run_initial_solution_value"] = best_run["@initial_solution_value"]
            result["@best_run_initial_solution_cost"] = best_run["@initial_solution_cost"]
            result["@best_run_solution_value"] = best_run["@solution_value"]
            result["@best_run_solution_cost"] = best_run["@solution_cost"]
            result["@best_run_solution_time"] = best_run["@runtime"]
            result["@best_run_solution_optimality"] = best_run["@solution_value"]/BKVs[result["@instance"]]
            result["@best_run_solution_seed"] = best_run["@seed"]
            result["@initial_solution_deviation"] = (best_run["@solution_value"] - best_run["@initial_solution_value"])/best_run["@initial_solution_value"]
            result["@solution_optimality_deviation"] = 1 - result["@best_run_solution_optimality"]
            result["@avg_solution_value"] = sum(map(lambda r: r["@solution_value"], exp_result["_runs"]))/len(exp_result["_runs"])
            result["@avg_solution_optimality"] = sum(map(lambda r: r["@solution_value"]/BKVs[result["@instance"]], exp_result["_runs"]))/len(exp_result["_runs"])
            result["@avg_solution_time"] = sum(map(lambda r: r["@runtime"], exp_result["_runs"]))/len(exp_result["_runs"])
            report.append(result)
        with open(f"soupreport-{report_id}.json", "w") as f:
            f.write(json.dumps(report))

# Create an output handler
def extract_results(run_info: dict, byte_array: bytes):
    output = byte_array.decode()
    for line in output.splitlines():
        if re.match(r'initial_solution_value:', line):
            run_info['@initial_solution_value'] = int(line.split(':')[1].strip())
        elif re.match(r'initial_solution_cost:', line):
            run_info['@initial_solution_cost'] = int(line.split(':')[1].strip())
        elif re.match(r'solution_value:', line):
            run_info['@solution_value'] = int(line.split(':')[1].strip())
        elif re.match(r'solution_cost:', line):
            run_info['@solution_cost'] = int(line.split(':')[1].strip())
        elif re.match(r'runtime:', line):
            run_info['@runtime'] = float(line.split(':')[1].strip())
        elif re.match(r'generations:', line):
            run_info['@generations'] = int(line.split(':')[1].strip())
        elif re.match(r'total_non_improving_generations:', line):
            run_info['@non_improving_generations'] = int(line.split(':')[1].strip())
        elif re.match(r'seed:', line):
            run_info['@seed'] = int(line.split(':')[1].strip())
