# AWS Bedrock deployment

This deployment keeps model credentials out of Cowork and every browser:

`browser -> OIDC login -> Cowork -> private LiteLLM gateway -> AWS Bedrock`

The gateway uses the AWS SDK default credential chain. On ECS, attach the
policy in `bedrock-task-role-policy.json` to the **task role** for the gateway;
do not put access keys in `.env`. PostgreSQL stores usage and cost records and
is required for the monthly budget to be enforced.

## Start

1. Enable the selected models in the Bedrock console in the chosen Region.
2. Copy `.env.example` to `.env` and replace every secret and OIDC value.
3. Register this callback URL with the OIDC provider:
   `https://YOUR_HOST/oauth2/callback`.
4. Put an HTTPS load balancer or reverse proxy in front of port 3000.
5. From this directory run:

   ```powershell
   docker compose up --build -d
   docker compose ps
   ```

Cowork uses the aliases `planning` and `coding`. Change their Bedrock targets
in `litellm-config.yaml`, or select `glm-4.7`/`nova-pro` through the two
`COWORK_*_MODEL` environment variables. Keep a model with vision and reliable
tool calling as the planning model because attachments, tools, structured
outputs, memory extraction, and artifact workflows depend on those features.

## Verify capabilities

Run the gateway smoke test from a trusted admin machine after temporarily
making the gateway reachable on localhost (or from inside its private network):

```powershell
$env:LITELLM_MASTER_KEY = "the-secret-from-.env"
$env:MODEL_GATEWAY_URL = "http://127.0.0.1:4000/v1"
python smoke_test.py
```

Then exercise Cowork end to end: create a conversation, stream a reply, upload
an image and a document, invoke a connector/tool, create an artifact, run a
scheduled task, and switch between Anton and Hermes.

## Boundaries

The current Cowork backend stores settings, projects, memory, connector
credentials, and conversations in one shared workspace. OIDC protects access,
but it does not isolate one user's data from another user's data. Deploy one
instance per trusted team or add tenant ownership and authorization checks to
the database/API before offering it to unrelated customers.

Channel webhooks and public artifact links require separate ingress routes with
provider signature verification; do not bypass OIDC for the entire `/api` path.
