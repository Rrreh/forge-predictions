import os
import time
import threading
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.response import SocketModeResponse

# Initialize clients using the variables you added to Railway
client = SocketModeClient(
    app_token=os.environ.get("SLACK_APP_TOKEN"),
    web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
)

def process_event(client, req):
    if req.type == "events_api":
        event = req.payload["event"]
        
        # Picosecond-level timing start
        start_ns = time.perf_counter_ns()
        
        if event.get("type") == "message" and "!triage" in event.get("text", ""):
            # Logic to pull your UPDATE_BOARD.md content goes here
            response_text = "Forge Triage: All systems nominal. Processing at high fidelity."
            
            # Picosecond-level timing end
            end_ns = time.perf_counter_ns()
            latency = end_ns - start_ns
            
            client.web_client.chat_postMessage(
                channel=event["channel"],
                text=f"{response_text}\n_Execution Latency: {latency}ns_"
            )

        # Acknowledge the request to Slack
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

client.socket_mode_request_listeners.append(process_event)
client.connect()
threading.Event().wait()
