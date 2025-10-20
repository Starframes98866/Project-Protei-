# Authentication

AGI Protei uses API key authentication.

## Getting an API Key
- Create an account at `https://project-protei.com`
- Generate an API key in your dashboard

## Using the API Key
- Set environment variable `PROTEI_API_KEY`
- Pass `apiKey` to SDK clients

## Revocation and Rotation
- Rotate keys regularly and immediately on leak suspicions
- Revoke compromised keys from the dashboard
