import base64
import os

from flask import Flask, request

from actions.hello_world import hello_world

app = Flask(__name__)


@app.route("/", methods=["POST"])
def handle_pubsub_message():
    envelope = request.get_json()
    if not envelope:
        return handle_errors(400, "No Pub/Sub message received")

    message = envelope.get("message")
    if not message:
        return handle_errors(400, "No message received")

    pubsub_message = base64.b64decode(message["data"]).decode("utf-8")
    print(f"Pub/Sub message received: {pubsub_message}")
    hello_world()

    return f"COMPLETED", 202


@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200


def handle_errors(status_code, msg):
    print(f"Error: {msg}")
    return f"Bad Request: {msg}", status_code


if __name__ == "__main__":
    debug = os.environ.get("ENV", "") == "DEV"
    app.run(debug=debug, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
