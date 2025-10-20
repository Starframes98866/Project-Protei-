# Node.js: Basic Completion

```ts
import { Protei } from "@agi-protei/sdk";

async function main() {
  const protei = new Protei({ apiKey: process.env.PROTEI_API_KEY });
  const result = await protei.completions.create({
    model: "protei-large",
    prompt: "Write a haiku about the sea",
  });
  console.log(result.text);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```
