import requests
import json

from app.enum.enums import Message, Color
from app.resource.discord_api import DiscordApi


class WorkItem:
    def __init__(self, webhook_id, webhook_token):
        self.discord_api = DiscordApi(webhook_id, webhook_token)
    
    def _color_switch(self, event_type) -> str:
        if event_type == "Created":
            return Color.GREEN.value
        elif event_type == "Deleted":
            return Color.RED.value
        elif event_type == "Restored":
            return Color.YELLOW.value
        elif event_type == "Updated":
            return Color.BLUE.value
        else:
            return Color.WHITE.value

    def webhook(self, data):
        try:
            event_type = data["eventType"].split(".")[1].capitalize()
            description = data["detailedMessage"]["markdown"]
            url = data["resource"]["url"]
            color = int(self._color_switch(event_type), 16)
            
            if event_type == "Updated":
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
                    "title": event_type,
                    "description": description,
                    "url": url,
                    "color": color,
                    "author": {
                        "name": author,
                        "icon_url": author_image
                    },
                    "footer": {
                        "text": event_type
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
