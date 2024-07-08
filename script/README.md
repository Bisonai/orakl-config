# Scripts

## Setup

```bash
# create virtual env called venv
python3 -m venv venv

# activate the venv
source venv/bin/activate

# install packages
pip install -r requirements.txt
```

Simply run `deactivate` for deactivating the venv.

## Generate Config Files

Automatically generates `configs.json` files based on supported WebSocket APIs.

### Parameters

- network: Designate network, defaults to `baobab`.
- refresh: true or false, defaults to false. Reload possible supported symbols from APIs if true.
- symbols: Pass symbols to generate besides pre-existing price pairs in the `configs/{network}/` path. If not given, it will only update existing config files.

```
python3 script/generate-configs.py --network cypress --refresh true --symbols "NOT-USDT, PEOPLE-USDT"
```

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
python script/generate-readme.py >! README.md
```

## Generate HISTORY.md

The `generate-history.py` script fetches all previous version of adapters and aggregators, and prints out them in markdown format to standard output.

Execute from root directory of this repository.

```
python script/generate-history.py >! HISTORY.md
```
