import json
import os
from pathlib import Path


def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)


def collect_adapter_files(adapter_dir: str, output_file_path: str):
    adapter_dir = Path(adapter_dir)
    adapter_files = list(adapter_dir.glob("*.json"))

    result = []
    for file in adapter_files:
        if file.name != "por.json":
            result.append(load_json_from_path(file))

    with open(output_file_path, "w") as f:
        json.dump({"adapters": result}, f, indent=4)


collect_adapter_files("adapter/baobab", "baobab_adapters.json")
collect_adapter_files("adapter/cypress", "cypress_adapters.json")
