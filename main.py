import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

# Initialize clients
web_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
app_token = os.environ.get("SLACK_APP_TOKEN")

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload.get("event", {})
        text = event.get("text", "")
        channel_id = event.get("channel")

        # Command Routing
        if text.startswith("!triage") or text.startswith("!predict"):
            web_client.chat_postMessage(
                channel=channel_id, 
                text="🚀 Forge is analyzing the latest market_edges.json..."
            )
            # Add your logic here to read JSON and reply

        # Acknowledge the event to Slack
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

# Connect and stay alive
rtm_client = SocketModeClient(app_token=app_token, web_client=web_client)
rtm_client.socket_mode_request_listeners.append(process)
rtm_client.connect()

from threading import Event
Event().wait()  # Keeps the script running continuously on Railway

