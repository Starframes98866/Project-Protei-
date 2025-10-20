# IDE Plugin Example

A filesystem utility plugin confined to a root (default `/workspace`). It supports:
- `ide.list(root?, path=".")`: List directory entries
- `ide.read(root?, path, max_bytes?)`: Read a file
- `ide.write(root?, path, content, encoding?)`: Write a text file
- `ide.search(root?, path=".", pattern, regex?, ignore_case?)`: Search text files

Run server:
```bash
python3 ./agi_protei/plugins/ide.py --serve
```

Config:
```yaml
plugins:
  - id: pytools
    kind: builtin_pytools
  - id: ide-ops
    kind: process
    command: ["python3", "./agi_protei/plugins/ide.py", "--serve"]
```

Try:
```bash
python3 -m agi_protei.cli --config ./config-ide.yaml invoke --tool ide.list --params '{"path":"."}'
python3 -m agi_protei.cli --config ./config-ide.yaml invoke --tool ide.write --params '{"path":"/workspace/DEMO.txt","content":"hello"}'
python3 -m agi_protei.cli --config ./config-ide.yaml invoke --tool ide.read --params '{"path":"/workspace/DEMO.txt"}'
python3 -m agi_protei.cli --config ./config-ide.yaml invoke --tool ide.search --params '{"path":"/workspace","pattern":"agi-protei"}'
```
