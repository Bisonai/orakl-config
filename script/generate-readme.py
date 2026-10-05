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
        try:
            data = load_json_from_path(config)
        except (json.JSONDecodeError, OSError) as err:
            print('skipping {}: invalid JSON ({})'.format(config, err), file=sys.stderr)
            continue

        feeds = data.get('feeds')
        if not isinstance(feeds, list):
            print('skipping {}: "feeds" missing, null, or not a list'.format(config), file=sys.stderr)
            continue

        missing = [k for k in ('fetchInterval', 'aggregateInterval', 'submitInterval') if k not in data]
        if missing:
            print('skipping {}: missing interval field(s): {}'.format(config, ', '.join(missing)), file=sys.stderr)
            continue

        values = []
        for key in keys:
            if key == 'feeds':
                values.append(len(feeds))
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
