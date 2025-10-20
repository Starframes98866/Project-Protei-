# Quickstart

This quickstart walks you through installing, configuring, and invoking AGI Protei in a minimal scenario.

## Prerequisites
- Linux or macOS
- Node.js >= 18 or Python >= 3.10 (choose one stack)

## Installation

### Option A: Node.js SDK
```bash
npm install @agi-protei/sdk
# or
pnpm add @agi-protei/sdk
```

### Option B: Python SDK
```bash
pip install agi-protei
```

## Basic Usage

### Node.js
```ts
import { Protei } from "@agi-protei/sdk";

const protei = new Protei({ apiKey: process.env.PROTEI_API_KEY });

const result = await protei.completions.create({
  model: "protei-large",
  prompt: "Summarize: ...",
});

console.log(result.text);
```

### Python
```python
from agi_protei import Protei

protei = Protei(api_key=os.environ["PROTEI_API_KEY"])

result = protei.completions.create(
    model="protei-large",
    prompt="Summarize: ...",
)

print(result.text)
```

## Next Steps
- See the API reference in `docs/api/README.md`
- Explore examples in `docs/examples`
