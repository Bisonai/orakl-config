import json
import os
from pathlib import Path

wsfetchers = ["binance", "coinbase", "coinone", "korbit"]

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

def define_websocket_feed(feed_name):
    wsFeed = {}
    for ws in wsfetchers:
        if ws in feed_name.lower():
            wsFeed["name"] = ws + "-wss-" + feed_name
            wsFeed["definition"] = {}
            wsFeed["definition"]["type"] = "wss"
            wsFeed["definition"]["provider"] = ws
            wsFeed["definition"]["base"] = feed_name.split("-")[-2]
            wsFeed["definition"]["quote"] = feed_name.split("-")[-1]
            break
    return wsFeed

def generate_config_files(adapter_path: Path, aggregator_path: Path, output_folder_path: str):
    adapters = load_json_files(adapter_path)
    aggregators = load_json_files(aggregator_path)
    configs = {}

    for adapter in adapters:
        config = {}
        config["name"] = adapter["name"]
        config["feeds"] = []

        for feed in adapter["feeds"]:
            wsFeed = define_websocket_feed(feed["name"])
            if wsFeed != {}:
                config["feeds"].append(wsFeed)
            else:
                config["feeds"].append(feed)
        config["fetchInterval"] = 2000

        configs[adapter["name"]] = config

    for aggregator in aggregators:
        if aggregator["name"] not in configs:
            continue
        configs[aggregator["name"]]["aggregateInterval"] = aggregator["aggregateHeartbeat"] if "aggregateHeartbeat" in aggregator else 5000
        configs[aggregator["name"]]["submitInterval"] = aggregator["heartbeat"] if "heartbeat" in aggregator else 15000

    for key, value in configs.items():
        with open(f"{output_folder_path}/{key}.config.json", "w") as f:
            json.dump(value, f, indent=4)




def generate_config_file(adapter_path: Path, aggregator_path: Path, output_file_path: str):
    temp_result = {}

    adapters = load_json_files(adapter_path)
    aggregators = load_json_files(aggregator_path)

    for adapter in adapters:
        for feed in adapter["feeds"]:
            for ws in wsfetchers:
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
    # generate_config_files(Path("adapter/test"), Path("aggregator/test"), "config/test")
    # generate_config_files(Path("adapter/baobab"), Path("aggregator/baobab"), "config/baobab")
    # generate_config_files(Path("adapter/cypress"), Path("aggregator/cypress"), "config/cypress")
    collect_json_files(Path("adapter/baobab"), "baobab_adapters.json")
    collect_json_files(Path("adapter/cypress"), "cypress_adapters.json")
    collect_json_files(Path("adapter/test"), "test_adapters.json")
    collect_json_files(Path("aggregator/baobab"), "baobab_aggregators.json")
    collect_json_files(Path("aggregator/cypress"), "cypress_aggregators.json")
    collect_json_files(Path("aggregator/test"), "test_aggregators.json")
    collect_json_files(Path("config/baobab"), "baobab_configs.json")
    collect_json_files(Path("config/cypress"), "cypress_configs.json")
    collect_json_files(Path("config/test"), "test_configs.json")
