import json
import os
from pathlib import Path

def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)


def collect_json_files(adapter_dir: Path, output_file_path: str):
    adapter_files = sorted(adapter_dir.glob("*.json"))

    result = []
    for file in adapter_files:
        if "por.json" not in file.name and "por-fast.json" not in file.name:
            result.append(load_json_from_path(file))

    with open(output_file_path, "w") as f:
        json.dump({"result": result}, f, indent=4)


if __name__ == "__main__":
    collect_json_files(Path("adapter/baobab"), "baobab_adapters.json")
    collect_json_files(Path("adapter/cypress"), "cypress_adapters.json")
    collect_json_files(Path("aggregator/baobab"), "baobab_aggregators.json")
    collect_json_files(Path("aggregator/cypress"), "cypress_aggregators.json")