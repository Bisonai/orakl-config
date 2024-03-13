import os
import sys
import json
from pathlib import Path


def make_line(words):
    for word in words:
        if type(word) != dict:
            if word == '':
                word = '-'
            print('| {} '.format(word), end='')
        else:
            print('| [{}]({}) '.format(word['value'], word['url']), end='')
    print('|')


def make_empty_line(words):
    for i in range(len(words)):
        print('|', '---', end=' ')
    print('|')


def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)


def collect_adapter_hashes(directory: Path):
    adapter_files = list(directory.glob("*.json"))

    data = {}
    for file in adapter_files:
        adapter_hash = load_json_from_path(file).get("adapterHash")
        if adapter_hash is None:
            raise RuntimeError(f"missing adapterHash in {file}")
        data[adapter_hash] = file.name

    return data


def generate_adapter_list(adapter_path: Path):
    adapters = sorted(adapter_path.glob("*.json"))
    keys = ['name', 'adapterHash', 'decimals', 'feeds']
    make_line(keys)
    make_empty_line(keys)
    for adapter in adapters:
        data = load_json_from_path(adapter)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': adapter, 'value': data[key]})
            else:
                values.append(data[key])
        make_line(values)


def generate_aggregator_list(aggregator_path: Path):
    aggregators = sorted(aggregator_path.glob("*.json"))
    keys = ['name', 'aggregatorHash', 'address', 'heartbeat', 'threshold', 'absoluteThreshold', 'adapterHash']
    make_line(keys)
    make_empty_line(keys)
    for aggregator in aggregators:
        filePath = os.path.join(aggregator)
        data = load_json_from_path(filePath)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': filePath, 'value': data[key]})
            else:
                values.append(data[key])
        make_line(values)


def check_hash_match(adapter_dir: Path, aggregator_dir: Path):
    adapters = collect_adapter_hashes(adapter_dir)
    aggregators = collect_adapter_hashes(aggregator_dir)
    for aggregator_adapter_hash, aggregator_name in aggregators.items():
        if aggregator_adapter_hash not in adapters:
            msg = f'Did not find corresponding adapterHash {aggregator_adapter_hash} for aggregator {aggregator_name}'
            raise Exception(msg)

        print(f'Matching {aggregator_name}: {aggregator_adapter_hash} with {adapters[aggregator_adapter_hash]}', file=sys.stderr)


if __name__ == "__main__":
    adapter_baobab_dir = Path('adapter/baobab')
    adapter_cypress_dir = Path('adapter/cypress')
    aggregator_baobab_dir = Path('aggregator/baobab/')
    aggregator_cypress_dir = Path('aggregator/cypress/')
    check_hash_match(adapter_baobab_dir, aggregator_baobab_dir)
    check_hash_match(adapter_cypress_dir, aggregator_cypress_dir)

    print('\n## Adapter Baobab\n')
    generate_adapter_list(adapter_baobab_dir)

    print('\n## Adapter Cypress\n')
    generate_adapter_list(adapter_cypress_dir)

    print('\n## Aggregator Baobab\n')
    generate_aggregator_list(aggregator_baobab_dir)

    print('\n## Aggregator Cypress\n')
    generate_aggregator_list(aggregator_cypress_dir)

    print("\n## Log history\n")
    print("[History of Adapter and Aggregator](HISTORY.md)")
