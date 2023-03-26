import requests
import json

from app.enum.enums import Message, Color


class DiscordApi:
    def __init__(self, discord_id, discord_token):
        self.base_url = "https://discord.com/api/webhooks"
        self.webhook_url = f'{self.base_url}/{discord_id}/{discord_token}'
        self.session = requests.Session()
        self.headers = {
            "Content-Type" : "application/json"
        }

    def post_webhook(self, body):
        result = self.session.post(self.webhook_url, data=json.dumps(body), headers=self.headers)
        
        if result.status_code == 204:
            return ({"message": Message.WEBHOOK_SUCCESS_MESSAGE.value})
        else:
            return result.text, result.status_code