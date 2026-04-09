# fls26-hack
Group Project of the Future Leader Summit 2026 Hackathon

## Run Locally

The server supports two modes controlled through `MCP_MODE`:

- `local`: easier local testing with stateless JSON responses
- `cloud`: deployment mode for Cloud Run and hosted clients such as LibreChat

Mode behavior:

- `local` binds to `127.0.0.1` and uses stateless JSON responses
- `cloud` binds to `0.0.0.0` and uses the stateful session-based Streamable HTTP flow
- If `MCP_MODE` is not set, the default is `cloud`
- This means the Cloud Run deployment flow stays the same as before

Local test mode:

```powershell
$env:MCP_MODE="local"
pip install -r requirements.txt
python mcp_server.py
```

The MCP server is exposed at `http://localhost:8000/mcp`.

Cloud-compatible local test mode:

```powershell
$env:MCP_MODE="cloud"
python mcp_server.py
```

Use `cloud` mode if you want to test the same session-based Streamable HTTP behavior that will run on Cloud Run.

## Test With `test.http`

The repository includes [`test.http`](d:/Workspace/fls26-hack/test.http) for manual MCP testing with the VS Code `REST Client` extension.

Local mode with `MCP_MODE=local`:

- Set `@baseUrl = http://localhost:8000`
- You can test the endpoint locally
- `local` mode is stateless and intended for easier debugging

Cloud-compatible mode with `MCP_MODE=cloud`:

- Set `@baseUrl = http://localhost:8000` for local cloud-style testing
- Or set `@baseUrl = https://YOUR_SERVICE_URL` for the deployed Cloud Run service
- Run `Step 1: Initialize MCP session` first
- Copy the `mcp-session-id` response header into `@sessionId`
- Then run `Step 2` through `Step 5`

Session handling:

- The `mcp-session-id` is returned as an HTTP response header, not in the JSON body
- A session ID from one initialization request cannot be reused forever
- If you get `Session not found`, initialize again and paste the new `mcp-session-id` into `@sessionId`
- In hosted mode, `Step 2` to `Step 5` require a valid `Mcp-Session-Id` header

## Deploy To Google Cloud Run

This project is set up for container deployment to Cloud Run.

Prerequisites:

- Install the Google Cloud SDK
- Log in with an account that has access to the target project
- Set the active project
- Run the commands from the repository root, not from a subfolder

```powershell
gcloud auth login
gcloud config set project PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

Build the image from the repo root:

```powershell
cd D:\Workspace\fls26-hack
gcloud builds submit --tag gcr.io/PROJECT_ID/fls26-mcp
```

Deploy the service:

```powershell
gcloud run deploy fls26-mcp `
  --image gcr.io/PROJECT_ID/fls26-mcp `
  --platform managed `
  --region europe-west3 `
  --allow-unauthenticated
```

Cloud Run uses the default `MCP_MODE=cloud`, so the deployment command still works without changes.

If you want to set it explicitly, you can deploy with:

```powershell
gcloud run deploy fls26-mcp `
  --image gcr.io/PROJECT_ID/fls26-mcp `
  --platform managed `
  --region europe-west3 `
  --allow-unauthenticated `
  --set-env-vars MCP_MODE=cloud
```

After deployment, the MCP endpoint is:

```text
https://YOUR_SERVICE_URL/mcp
```

If your server uses API keys, set them in Cloud Run instead of shipping the local `.env` file:

```powershell
gcloud run deploy fls26-mcp `
  --image gcr.io/PROJECT_ID/fls26-mcp `
  --platform managed `
  --region europe-west3 `
  --allow-unauthenticated `
  --set-env-vars OPENAI_API_KEY=YOUR_KEY,GOOGLE_API_KEY=YOUR_KEY
```

Important notes:

- The service URL root is not the MCP endpoint. Use `/mcp`.
- A successful example endpoint looks like `https://YOUR_SERVICE_URL/mcp`.
- If `gcloud builds submit --tag ...` says `Dockerfile required when specifying --tag`, you are in the wrong directory.
- `.env` is excluded from the container build by `.dockerignore`.
- `MCP_MODE=local` is intended for local testing only.
- `MCP_MODE=cloud` is the mode for Cloud Run and LibreChat.

## LibreChat

For LibreChat, configure the hosted MCP server with:

- URL: `https://YOUR_SERVICE_URL/mcp`
- Transport: `Streamable HTTPS`
- Authentication: `None`

If the MCP server works in `test.http` but not in LibreChat, first verify that LibreChat is using the `/mcp` path and not only the service root URL.
