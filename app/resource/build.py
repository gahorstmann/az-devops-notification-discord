import requests
import json

from app.enum.enums import Message, Color


class WorkItem:
    def __init__(self, event_type, discord_id, discord_token):
        self.event_type = event_type
        self.base_url = "https://discord.com/api/webhooks"
        self.webhook_url = f'{self.base_url}/{discord_id}/{discord_token}'
        self.session = requests.Session()
        self.headers = {
            "Content-Type" : "application/json"
        }
