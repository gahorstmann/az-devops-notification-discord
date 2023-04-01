import json

from flask import Blueprint, request

from app.models.work_item import WorkItem
from app.models.build import Build
from app.models.pull_request import PullRequest
from app.utils import Message


routes = Blueprint('routes', __name__)

@routes.route("/", methods=["POST"])
def hook():
    webhook_id = request.headers.get('discord-id')
    webhook_token = request.headers.get('discord-token')
    
    #Validate Header
    if not webhook_id or not webhook_token:
        return ({'error': Message.HEADER_REQUIRED_MESSAGE.value}), 400
    
    #Validate JSON
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return ({'error': Message.JSON_ERROR.value}), 400 
    
    method = data["eventType"].split(".")
    settings = method[0], webhook_id, webhook_token
    
    if method[0] == "workitem":
        work_item = WorkItem(settings)
        return work_item.webhook(method[1], data)
    
    if method[0] == "build":
        build = Build(settings)
        return build.webhook(data)
    
    if f"{method[0]}.{method[1]}" in ["ms.vss-code", "git.pullrequest"]:
        pull_request = PullRequest(settings)
        return pull_request.webhook(method[2], data)
    
    return ({'error': Message.EVENT_TYPE_ERROR_MESSAGE.value}), 404
