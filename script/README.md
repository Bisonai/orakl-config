# Scripts

## Collect All Adapter Files

The following script will gather all adapter configurations for baobab and cypress, and generate a single JSON file for for each network (`baobab_adapters.json` and `cypress_adapters.json` respectively).

Execute from root directory of this repository.

```
python script/collect-adapter-files.py
```

## Generate README.md

The `generate-readme.py` script will check whether all connections between aggregators and adapters are valid, and prints out new version of README to standard output.

Execute from root directory of this repository.

```
python script/generate-readme.py > README.m
```
