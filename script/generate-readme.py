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
        except (ValueError, OSError) as err:
            # ValueError covers JSONDecodeError and UnicodeDecodeError
            print('skipping {}: could not read/parse JSON ({})'.format(config, err), file=sys.stderr)
            continue

        if not isinstance(data, dict):
            print('skipping {}: top-level JSON is not an object'.format(config), file=sys.stderr)
            continue

        feeds = data.get('feeds')
        if not isinstance(feeds, list):
            print('skipping {}: "feeds" missing, null, or not a list'.format(config), file=sys.stderr)
            continue

        # Validate type, not just presence: a present-but-wrong-typed value
        # (e.g. an object or null) would otherwise reach make_line and either
        # abort (dict -> KeyError) or render a literal 'None' cell. Intervals
        # accept any JSON number (int or float) but not bool, which subclasses
        # int yet is not a valid interval.
        def valid_scalar(key, value):
            if key == 'name':
                return isinstance(value, str)
            return isinstance(value, (int, float)) and not isinstance(value, bool)

        bad = [k for k in ('name', 'fetchInterval', 'aggregateInterval', 'submitInterval')
               if not valid_scalar(k, data.get(k))]
        if bad:
            print('skipping {}: field(s) missing or not the expected type: {}'.format(config, ', '.join(bad)), file=sys.stderr)
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
