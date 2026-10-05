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

The `generate-readme.py` script prints the per-pair interval tables to standard output: one markdown section per network for the `config/<network>/` pairs (`## Config Baobab`, `## Config Cypress`) followed by one per network for the `mag7/<network>/` feeds (`## Mag7 Baobab`, `## Mag7 Cypress`). The mag7 schema differs — it has no `aggregateInterval`/`submitInterval`, so the mag7 sections use their own columns (`name | interval | heartbeat | threshold | feeds`). The links are repo-root-relative, so the output is meant to be read against the repo root. The tables are not committed to `README.md`; run the script on demand. Do not redirect the output into `README.md` — that file is now hand-written prose, not generated.

Execute from root directory of this repository.

```
python script/generate-readme.py
```
