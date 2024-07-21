import json
import time
from kiwi.reporter import BaseReporter

BKVs = {
    "ep01": 2118,
    "ep02": 1378,
    "ep03": 2850,
    "ep04": 2730,
    "ep05": 2624,
    "ep06": 4690,
    "ep07": 4440,
    "ep08": 5020,
    "ep09": 4568,
    "ep10": 4390,
}

class SoupReporter(BaseReporter):
    @staticmethod
    def generate(results: list[dict]):
        report_id = time.time_ns()
        report = []
        for exp_result in results:
            result = dict()
            name: str = exp_result["name"]
            name = name.split("-")
            result["@instance"] = f"{name[0]}.dat"
            result["@population_size"] = int(name[1][1:])
            result["@recombination_rate"] = float(name[2][1:])
            result["@mutation_rate"] = float(name[3][1:])
            best_run = max(exp_result["_runs"], key=lambda r: r["@solution_value"])
            result["@best_solution_value"] = best_run["@solution_value"]
            result["@best_solution_cost"] = best_run["@solution_cost"]
            result["@best_solution_time"] = best_run["@runtime"]
            result["@best_solution_optimality"] = best_run["@solution_value"]/BKVs[name[0]]
            result["@best_solution_seed"] = best_run["@seed"]
            result["@avg_solution_value"] = sum(map(lambda r: r["@solution_value"], exp_result["_runs"]))/len(exp_result["_runs"])
            report.append(result)
        with open(f"soupreport-{report_id}.json", "w") as f:
            f.write(json.dumps(report))

