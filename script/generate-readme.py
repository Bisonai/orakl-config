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

def generate_config_list(config_dir: Path):
    configs = sorted(config_dir.glob("*.json"))
    keys = ['name', 'fetchInterval', 'aggregateInterval', 'submitInterval', 'feeds']
    make_line(keys)
    make_empty_line(keys)
    for config in configs:
        data = load_json_from_path(config)
        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(data[key]))
            elif key == 'name':
                values.append({'url': config, 'value': data[key]})
            else:
                values.append(data[key])
        make_line(values)


if __name__ == "__main__":
    baobab = "baobab"
    cypress = "cypress"

    print('\n## Config Baobab\n')
    generate_config_list(Path('config') / baobab)

    print('\n## Config Cypress\n')
    generate_config_list(Path('config') / cypress)

    print("\n## Log history\n")
    print("[History of Adapter and Aggregator](HISTORY.md)")
