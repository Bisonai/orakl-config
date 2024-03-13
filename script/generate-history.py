import json
import os
from subprocess import PIPE, Popen
from pathlib import Path
from typing import List


def load_json_from_path(file_path: Path):
    with open(file_path) as json_file:
        return json.load(json_file)


def make_line(words: List) -> None:
    for word in words:
        if type(word) == dict:
            print("| [{}]({}) ".format(word["value"], word["url"]), end="")
        elif type(word) == list:
            print("| ", end="")
            for version in word:
                print("[{}]({})".format(version["value"], version["url"]), end="")
                if version != word[-1]:
                    print(", ", end="")
        else:
            if word == "":
                word = "-"
            print("| {} ".format(word), end="")
    print(" |")


def make_empty_line(words: List[str]) -> None:
    for i in range(len(words)):
        print("| ", "---", end=" ")
    print(" |")


def get_url_list(file_path: Path):
    # https://git-scm.com/docs/pretty-formats
    command = 'git log --branches master --pretty=format:"%H" {}'.format(file_path)
    process = Popen(command, stdout=PIPE, stderr=None, shell=True)
    commit_list = process.communicate()[0].decode("utf-8").splitlines()

    orakl_config_path = "https://github.com/Bisonai/orakl-config/blob/"
    url_list = []

    for index, commit in enumerate(reversed(commit_list)):
        url = "{}{}/{}".format(orakl_config_path, commit, file_path)
        version = "v" + str(index + 1)
        url_list.append({"url": url, "value": version})
    return url_list


def get_file_name(file_path: Path):
    return load_json_from_path(file_path)["name"]


def generate_history(directory: Path):
    json_files = sorted(directory.glob("*.json"))
    keys = ["Filename", "History"]
    make_line(keys)
    make_empty_line(keys)
    for file in json_files:
        filename = get_file_name(file)
        url_list = get_url_list(file)
        make_line([filename, url_list])

if __name__ == "__main__":
    adapter_dir = Path("adapter")
    aggregator_dir = Path("aggregator")

    print("\n# History\n")

    print("\n## Adapter Baobab\n")
    generate_history(adapter_dir / "baobab")

    print("\n## Adapter Cypress\n")
    generate_history(adapter_dir / "cypress")

    print("\n## Aggregator Baobab\n")
    generate_history(aggregator_dir / "baobab")

    print("\n## Aggregator Cypress\n")
    generate_history(aggregator_dir / "cypress")
