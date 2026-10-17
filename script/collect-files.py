import argparse
import json
import sys
from pathlib import Path

wsfetchers = ["binance", "coinbase", "coinone", "korbit", "kucoin", "bybit", "upbit", "crypto", "btse", "bithumb", "gateio", "huobi", "mexc", "orangex"]

def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)

def load_json_files(directory: Path):
    files = sorted(directory.glob("*.json"))

    result = []
    for file in files:
        with open(file) as json_file:
            result.append(json.load(json_file))

    return result

def collect_json_files(directory: Path, output_file_path: str, wrap=True):
    result = load_json_files(directory)
    with open(output_file_path, "w") as f:
        if wrap:
            json.dump({"result": result}, f, indent=4)
        else:
            json.dump(result, f, indent=4)

def filter_invalid_configs(configs: list):
    result = []
    for config in configs:
        if "feeds" not in config or len(config["feeds"]) == 0:
            continue
        result.append(config)
    return result

def define_websocket_feed(feed_name, adapter_name):
    wsFeed = {}
    for ws in wsfetchers:
        if ws in feed_name.lower():
            wsFeed["name"] = ws + "-wss-" + adapter_name
            wsFeed["definition"] = {}
            wsFeed["definition"]["type"] = "wss"
            wsFeed["definition"]["provider"] = ws
            wsFeed["definition"]["base"] = feed_name.split("-")[-2]
            wsFeed["definition"]["quote"] = feed_name.split("-")[-1]
            break
    return wsFeed

def update_config_file_websocket(config_path: Path):
    configs = load_json_files(config_path)
    for config in configs:
        for feed in config["feeds"]:
            wsFeed = define_websocket_feed(feed["name"], config["name"])
            if wsFeed != {}:
                print("update feed", feed["name"], "to", wsFeed["name"])
                feed["name"] = wsFeed["name"]
                feed["definition"] = wsFeed["definition"]


        with open(f"{config_path}/{config['name']}.config.json", "w") as f:
            json.dump(config, f, indent=4)

def generate_config_files(adapter_path: Path, aggregator_path: Path, output_folder_path: str):
    adapters = load_json_files(adapter_path)
    aggregators = load_json_files(aggregator_path)
    configs = {}

    for adapter in adapters:
        config = {}
        config["name"] = adapter["name"]
        config["feeds"] = []

        for feed in adapter["feeds"]:
            wsFeed = define_websocket_feed(feed["name"], adapter["name"])
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

ROOT = Path(__file__).resolve().parent.parent

# (source dir, served bundle) pairs, relative to the repo root (ROOT).
BUNDLES = [
    ("config/kairos", "kairos_feeds.json"),
    ("config/mainnet", "mainnet_feeds.json"),
    ("mag7/kairos", "kairos_mag7.json"),
    ("mag7/mainnet", "mainnet_mag7.json"),
]

def load_for_check(path: Path, label: str, errors: list):
    try:
        return load_json_from_path(path)
    except (OSError, ValueError) as e:
        errors.append(f"{label}: cannot load: {e}")
        return None

def canon(value):
    # Type-strict, key-order-insensitive form: 1 != 1.0 != true.
    return json.dumps(value, sort_keys=True)

def is_named_list(value):
    return isinstance(value, list) and all(isinstance(e, dict) and isinstance(e.get("name"), str) for e in value)

def by_name(entries, label: str, errors: list):
    # None (load failed, already reported) or bad shape -> None.
    if entries is None:
        return None
    if not is_named_list(entries):
        errors.append(f"{label}: expected a JSON list of objects with string \"name\"")
        return None
    result = {}
    for entry in entries:
        name = entry["name"]
        if name in result:
            errors.append(f"{label}: duplicate name {name!r}")
        result[name] = entry
    return result

def diff_feeds(gen_feeds, com_feeds):
    if not (is_named_list(gen_feeds) and is_named_list(com_feeds)):
        return ["feeds differ (not a list of objects with string \"name\")"]
    details = []
    gen_map = {f["name"]: f for f in gen_feeds}
    com_map = {f["name"]: f for f in com_feeds}
    for feed in sorted(gen_map.keys() - com_map.keys()):
        details.append(f"feed {feed} missing from bundle")
    for feed in sorted(com_map.keys() - gen_map.keys()):
        details.append(f"feed {feed} only in bundle")
    for feed in sorted(gen_map.keys() & com_map.keys()):
        if canon(gen_map[feed]) != canon(com_map[feed]):
            details.append(f"feed {feed} differs")
    if len(gen_map) != len(gen_feeds) or len(com_map) != len(com_feeds):
        details.append("duplicate feed names")
    elif [f["name"] for f in gen_feeds if f["name"] in com_map] != [f["name"] for f in com_feeds if f["name"] in gen_map]:
        details.append("feed order differs")
    return details

def check_bundle(source_dir: Path, bundle_path: Path, root: Path = ROOT):
    # Semantic check (#260): compare parsed JSON, not bytes, so cosmetic
    # serialization deltas (#236: indent, key order) are tolerated. Entries are
    # matched by "name": entry order in the bundle is ignored (node admin sync
    # keys configs by name). Within an entry, values (types included) and feed
    # order must match exactly.
    errors = []
    if not (root / source_dir).is_dir():
        return [f"{source_dir}/: source directory not found"]
    sources = [load_for_check(f, str(f.relative_to(root)), errors) for f in sorted((root / source_dir).glob("*.json"))]
    if errors:
        return errors
    generated = by_name(sources, str(source_dir), errors)
    committed = by_name(load_for_check(root / bundle_path, str(bundle_path), errors), str(bundle_path), errors)
    if generated is None or committed is None:
        return errors
    for name in sorted(generated.keys() - committed.keys()):
        errors.append(f"{name}: in {source_dir}/ but missing from {bundle_path}")
    for name in sorted(committed.keys() - generated.keys()):
        errors.append(f"{name}: in {bundle_path} but not in {source_dir}/")
    for name in sorted(generated.keys() & committed.keys()):
        gen, com = generated[name], committed[name]
        if canon(gen) == canon(com):
            continue
        details = []
        def show(entry, key):
            return canon(entry[key]) if key in entry else "(missing)"
        for key in sorted(gen.keys() | com.keys()):
            if key == "feeds":
                continue
            if show(gen, key) != show(com, key):
                details.append(f"{key}: {source_dir}/={show(gen, key)} bundle={show(com, key)}")
        if canon(gen.get("feeds")) != canon(com.get("feeds")):
            details += diff_feeds(gen.get("feeds"), com.get("feeds"))
        errors.append(f"{name}: " + "; ".join(details or ["differs"]))
    return errors

def check_bundles():
    failed = False
    for source_dir, bundle in BUNDLES:
        errors = check_bundle(Path(source_dir), Path(bundle))
        if errors:
            failed = True
            print(f"::error::{bundle} does not match {source_dir}/ ({len(errors)} problem(s))")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"{bundle}: OK")
    return 1 if failed else 0

if __name__ == "__main__":
    # Canonical bundles only: price feeds "<chain>_feeds.json" and mag7
    # "<chain>_mag7.json" for chains mainnet (Kaia mainnet) and kairos (testnet).
    # The old cypress/baobab + *_configs.json aliases were retired in Phase 5.
    #
    # NOTE (#236): the committed *_feeds.json bundles are FROZEN to pre-existing
    # bytes; the source config/ files differ by a cosmetic serialization delta
    # (indent 2->4 + key order), so running this WILL rewrite them — do not
    # commit that delta here. Use --check (CI, #260) to verify the bundles
    # semantically match their sources without writing anything.
    parser = argparse.ArgumentParser(description="Collect config/ and mag7/ sources into served bundles.")
    parser.add_argument("--check", action="store_true", help="exit 1 if a served bundle does not semantically match its source dir; writes nothing")
    args = parser.parse_args()
    if args.check:
        sys.exit(check_bundles())
    for source_dir, bundle in BUNDLES:
        collect_json_files(ROOT / source_dir, ROOT / bundle, False)
