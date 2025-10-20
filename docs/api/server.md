# Server Module

Server endpoints and deployment patterns.

> Placeholder: Populate with real exports when source is added.

## REST Endpoints
- `POST /v1/completions`
- `POST /v1/embeddings`

## Example cURL
```bash
curl -X POST "$PROTEI_BASE_URL/v1/completions" \
  -H "Authorization: Bearer $PROTEI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "protei-large",
    "prompt": "Hello"
  }'
```
