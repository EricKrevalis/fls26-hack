# fls26-hack
Group Project of the Future Leader Summit 2026 Hackathon

## Run Locally

```powershell
pip install -r requirements.txt
python mcp_server.py
```

The MCP server is exposed at `http://localhost:8000/mcp`.

## Deploy To Google Cloud Run

This project is set up for container deployment to Cloud Run.

Build the image:

```powershell
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

After deployment, the MCP endpoint is:

```text
https://YOUR_SERVICE_URL/mcp
```

Do not deploy the local `.env` file. In Cloud Run, set secrets or environment variables in the service configuration instead.
