# Usage Guide

This guide covers authentication, error handling, retries, and performance tips.

## Authentication
- Use an API key via `PROTEI_API_KEY` environment variable
- For server-side applications, load from secure secret storage

## Errors and Retries
- 429: backoff with jitter (e.g., exponential 100ms-2000ms)
- 5xx: retry up to 3 times; log correlation IDs
- Client-side validation errors: do not retry; fix inputs

## Timeouts
- Client default timeout: 60s; adjust based on model latency

## Streaming
- Prefer streaming for long responses to reduce latency to first token

## Concurrency
- Limit concurrent requests per process based on CPU and rate limits

## Security
- Never expose API keys to browsers
- Redact prompts and responses in logs when containing PII

## Observability
- Capture request IDs and latency metrics
- Record token usage for cost tracking
