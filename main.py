import os
from fastapi import FastAPI, Request
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

app = FastAPI()

# Railway will provide these via your Variables tab
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")

client = WebClient(token=SLACK_BOT_TOKEN)
verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

@app.get("/health")
def health_check():
    # Railway uses this to confirm the "Train has arrived"
    return {"status": "online", "agent": "Forge-Bot", "station": "arrived"}
@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    
    # This is the "Challenge" fix Slack is looking for
    if "challenge" in data:
        return {"challenge": data["challenge"]}
        
    return {"status": "ok"}
    # This handles the Slack handshake and commands
    body = await request.body()
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # Railway provides the PORT variable automatically
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
