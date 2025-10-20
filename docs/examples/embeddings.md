# Embeddings

## Node.js
```ts
import { Protei } from "@agi-protei/sdk";

const protei = new Protei({ apiKey: process.env.PROTEI_API_KEY });
const { vectors } = await protei.embeddings.create({ model: "protei-embed", input: ["hello", "world"] });
console.log(vectors.length);
```

## Python
```python
from agi_protei import Protei

protei = Protei(api_key=os.environ["PROTEI_API_KEY"])

vectors = protei.embeddings.create(model="protei-embed", input=["hello", "world"]).vectors
print(len(vectors))
```
