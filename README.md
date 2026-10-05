# orakl-config

Price-feed configuration for the Orakl Network oracle, per network (`baobab`, `cypress`).

## Layout

- `config/<network>/<PAIR>.config.json` — per-pair feed definitions (fetch / aggregate / submit intervals and the data-source feeds).
- `mag7/<network>/<name>.json` — mag7 feed definitions.
- `<network>_configs.json` / `<network>_mag7.json` — aggregated bundles served from the repo root.

## Per-pair table

The per-pair interval table (`name | fetchInterval | aggregateInterval | submitInterval | feeds`) for the `config/<network>/` pairs, plus a separate mag7 table (`name | interval | heartbeat | threshold | feeds`) for the `mag7/<network>/` feeds, is not committed. Regenerate both on demand with:

```
python script/generate-readme.py
```

See [`script/README.md`](script/README.md) for all scripts and setup.
