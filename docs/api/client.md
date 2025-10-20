# Client Module

Client-side helpers to integrate AGI Protei.

> Placeholder: Populate with real exports when source is added.

## Exports
- `CompletionsClient`
- `EmbeddingsClient`

## Examples
```ts
import { CompletionsClient } from "@agi-protei/sdk";

const completions = new CompletionsClient({ apiKey: process.env.PROTEI_API_KEY });
const res = await completions.create({ model: "protei-large", prompt: "Hi" });
console.log(res.text);
```
