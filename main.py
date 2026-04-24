import os
from fastapi import FastAPI, Request
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

app = FastAPI()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

client = WebClient(token=SLACK_BOT_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

@app.get("/health")
def health_check():
    return {"status": "online", "agent": "Forge-Bot"}

@app.post("/slack/events")
async def slack_events(request: Request):
    body = await request.body()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
