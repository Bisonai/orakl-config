import json
import os
from pathlib import Path

def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)

def load_json_files(directory: Path):
    files = sorted(directory.glob("*.json"))

    result = []
    for file in files:
        if "por.json" not in file.name and "por-fast.json" not in file.name:
            with open(file) as json_file:
                result.append(json.load(json_file))

    return result

def collect_json_files(directory: Path, output_file_path: str):
    result = load_json_files(directory)
    with open(output_file_path, "w") as f:
        json.dump({"result": result}, f, indent=4)

def filter_invalid_configs(configs: list):
    result = []
    for config in configs:
        if "feeds" not in config or len(config["feeds"]) == 0:
            continue
        result.append(config)
    return result

def generate_config_file(adapter_path: Path, aggregator_path: Path, output_file_path: str):
    temp_result = {}

    adapters = load_json_files(adapter_path)
    aggregators = load_json_files(aggregator_path)

    for adapter in adapters:
        for feed in adapter["feeds"]:
            for ws in ["binance", "coinbase", "coinone", "korbit"]:
                if ws in feed["name"].lower():
                    feed["name"] = ws + "-wss-" + adapter["name"]
                    feed["definition"] = {}
                    feed["definition"]["type"] = "wss"

        temp_result[adapter["name"]] = {}
        temp_result[adapter["name"]]["name"] = adapter["name"]
        temp_result[adapter["name"]]["feeds"] = adapter["feeds"]


        temp_result[adapter["name"]]["fetchInterval"] = adapter["interval"] if "interval" in adapter else 2000

    for aggregator in aggregators:
        if aggregator["name"] not in temp_result:
            temp_result[aggregator["name"]] = {}

        temp_result[aggregator["name"]]["aggregateInterval"] = aggregator["aggregateHeartbeat"] if "aggregateHeartbeat" in aggregator else 5000
        temp_result[aggregator["name"]]["submitInterval"] = aggregator["heartbeat"] if "heartbeat" in aggregator else 15000

    valid_configs = filter_invalid_configs(list(temp_result.values()))

    with open(output_file_path, "w") as f:
        json.dump(valid_configs, f, indent=4)

if __name__ == "__main__":
    collect_json_files(Path("adapter/baobab"), "baobab_adapters.json")
    collect_json_files(Path("adapter/cypress"), "cypress_adapters.json")
    collect_json_files(Path("adapter/test"), "test_adapters.json")
    collect_json_files(Path("aggregator/baobab"), "baobab_aggregators.json")
    collect_json_files(Path("aggregator/cypress"), "cypress_aggregators.json")
    collect_json_files(Path("aggregator/test"), "test_aggregators.json")

    generate_config_file(Path("adapter/test"), Path("aggregator/test"), "test_configs.json")
    # generate_config_file(Path("adapter/baobab"), Path("aggregator/baobab"), "baobab_configs.json")
    # generate_config_file(Path("adapter/cypress"), Path("aggregator/cypress"), "cypress_configs.json")
