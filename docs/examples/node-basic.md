# Node Plugin Example

A trivial Node-based plugin that supports `string.reverse`.

```bash
node ./plugins/node/basic.js --serve
```

Add to `config.yaml`:

```yaml
plugins:
  - id: pytools
    kind: builtin_pytools
  - id: node-basic
    kind: process
    optional: true
    command: ["node", "./plugins/node/basic.js", "--serve"]
```

Then:

```bash
agi-protei --config ./config.yaml list-plugins
agi-protei --config ./config.yaml invoke --tool string.reverse --params '{"text":"abc"}'
```
