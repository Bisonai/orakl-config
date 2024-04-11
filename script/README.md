# Scripts

## Collect Files

The following script will gather all adapter & aggregator configurations for baobab and cypress, and generate JSON files for for each network
Execute from root directory of this repository.

```
python script/collect-files.py
```

## Generate README.md

The `generate-readme.py` script will check whether all connections between aggregators and adapters are valid, and prints out new version of README to standard output.

Execute from root directory of this repository.

```
python script/generate-readme.py > README.md
```

## Generate HISTORY.md

The `generate-history.py` script fetches all previous version of adapters and aggregators, and prints out them in markdown format to standard output.

Execute from root directory of this repository.

```
python script/generate-history.py > HISTORY.md
```
