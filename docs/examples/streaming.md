# Streaming Completions

## Node.js
```ts
import { Protei } from "@agi-protei/sdk";

const protei = new Protei({ apiKey: process.env.PROTEI_API_KEY });
const stream = await protei.completions.stream({ model: "protei-large", prompt: "Explain transformers" });

for await (const chunk of stream) {
  process.stdout.write(chunk.text);
}
```

## Python
```python
from agi_protei import Protei

protei = Protei(api_key=os.environ["PROTEI_API_KEY"])

for chunk in protei.completions.stream(model="protei-large", prompt="Explain transformers"):
    print(chunk.text, end="")
```
