import os
import json

from flask import Flask, request
from app.resource.work_item import WorkItem
from app.enum.enums import Message

PORT = int(os.environ.get('PORT', 5000))

app = Flask (__name__)

@app.route("/", methods=["POST"])
def hook():
    webhook_id = request.headers.get('discord-id')
    webhook_token = request.headers.get('discord-token')
    
    if not webhook_id or not webhook_token:
        return ({'error': Message.HEADER_REQUIRED_MESSAGE.value}), 400
    
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return ({'error': Message.JSON_ERROR.value}), 400 
    
    method = data["eventType"].split(".")
    if method[0] == "workitem":
        work_item = WorkItem("", webhook_id, webhook_token)
        return work_item.webhook(data)
    
    return ({'error': Message.EVENT_TYPE_ERROR_MESSAGE.value}), 404

if __name__ == "__main__":
    app.run(port=PORT)
