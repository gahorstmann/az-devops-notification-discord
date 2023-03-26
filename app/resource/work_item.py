import requests
import json

from app.enum.enums import Message, Color
from app.resource.discord_api import DiscordApi


class WorkItem:
    def __init__(self, type, webhook_id, webhook_token):
        self.type = type
        self.discord_api = DiscordApi(webhook_id, webhook_token)
    
    def _color_switch(self, value) -> str:
        if value == "created":
            return Color.GREEN.value
        elif value == "deleted":
            return Color.RED.value
        elif value == "restored":
            return Color.YELLOW.value
        elif value == "updated":
            return Color.BLUE.value
        else:
            return Color.WHITE.value

    def webhook(self, type, data):
        try:
            description = data["detailedMessage"]["markdown"]
            url = data["resource"]["url"]
            color = int(self._color_switch(type), 16)
            
            if type == "updated":
                author = data["resource"]["revisedBy"]["displayName"]
                author_image = data["resource"]["revisedBy"]["_links"]["avatar"]["href"]
                
                created_date = data["resource"]["revisedDate"]
            else:
                author = data["resource"]["fields"]["System.CreatedBy"]["displayName"]
                author_image = data["resource"]["fields"]["System.CreatedBy"]["_links"]["avatar"]["href"]
            
                created_date = data["resource"]["fields"]["System.CreatedDate"]
                
            body = {
                "content": None,
                "embeds": [
                    {
                    "title": f'Work Item: {type.capitalize()}',
                    "description": description,
                    "url": url,
                    "color": color,
                    "author": {
                        "name": author,
                        "icon_url": author_image
                    },
                    "footer": {
                        "text": f'{type.capitalize()} at'
                    },
                    "timestamp": created_date
                    }
                ],
                "username": "Azure Devops",
                "attachments": []
            }
            
            return self.discord_api.post_webhook(body)
                
        except KeyError as e:
            return ({"error": Message.KEY_ERROR_MESSAGE.value.format(e.args[0].upper())}), 400
