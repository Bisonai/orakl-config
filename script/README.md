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
- onlysymbols: defaults to false, only reload supported symbols if true without generating configs

```
python3 script/generate-configs.py --network cypress --refresh true --symbols "NOT-USDT, PEOPLE-USDT"
```

## Collect Files

The following script will gather all adapter & aggregator configurations for baobab and cypress, and generate JSON files for for each network
Execute from root directory of this repository.

```
python script/collect-files.py
```

## Generate per-pair table

The `generate-readme.py` script prints the per-pair interval tables for the `config/<network>/` pairs — one markdown section per network (`## Config Baobab`, `## Config Cypress`) — to standard output. The pair links are repo-root-relative, so the output is meant to be read against the repo root. The tables are not committed to `README.md`; run the script on demand.

Execute from root directory of this repository.

```
python script/generate-readme.py
```
