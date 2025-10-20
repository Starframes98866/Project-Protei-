# Python: Basic Completion

```python
import os
from agi_protei import Protei

protei = Protei(api_key=os.environ["PROTEI_API_KEY"])

result = protei.completions.create(
    model="protei-large",
    prompt="Write a haiku about the sea",
)

print(result.text)
```
