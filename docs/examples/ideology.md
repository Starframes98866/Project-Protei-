# Ideology Plugin Example

A neutral, informational plugin with capabilities:
- `ideology.info`: Returns high-level summaries and core principles for ideologies like "communism", "socialism", and "capitalism".
- `ideology.compare`: Provides brief similarities/differences between two named ideologies.

Run server:
```bash
python3 ./agi_protei/plugins/ideology.py --serve
```

Config:
```yaml
plugins:
  - id: pytools
    kind: builtin_pytools
  - id: ideology
    kind: process
    command: ["python3", "./agi_protei/plugins/ideology.py", "--serve"]
```

Try:
```bash
python3 -m agi_protei.cli --config ./config-ideology.yaml invoke --tool ideology.info --params '{"topic":"communism"}'
python3 -m agi_protei.cli --config ./config-ideology.yaml invoke --tool ideology.compare --params '{"a":"communism","b":"capitalism"}'
```
