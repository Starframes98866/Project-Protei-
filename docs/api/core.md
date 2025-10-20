# Core Module

Public primitives and utilities for AGI Protei.

> Placeholder: Populate with real exports when source is added.

## Exports
- `Protei` class: top-level client
- `CompletionParams` type
- `EmbeddingParams` type

## Example
```ts
import { Protei } from "@agi-protei/sdk";

const client = new Protei({ apiKey: process.env.PROTEI_API_KEY });
const out = await client.completions.create({ model: "protei-large", prompt: "Hello" });
console.log(out.text);
```
