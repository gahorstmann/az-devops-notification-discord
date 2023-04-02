from app.utils import Message, Color
from app.models.discord_api import DiscordApi


class WorkItem:
    def __init__(self, settings):
        self.type = settings[0]
        self.discord_api = DiscordApi(settings[1], settings[2])
    
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
            title = f"Work Item: {type.capitalize()}"
            description = data["detailedMessage"]["markdown"]
            url = data["resource"]["url"]
            color = int(self._color_switch(type), 16)
            
            if type == "updated":
                author = data["resource"]["revisedBy"]["displayName"]
                author_image = data["resource"]["revisedBy"]["_links"]["avatar"]["href"]
                
                time = data["resource"]["revisedDate"]
            else:
                author = data["resource"]["fields"]["System.CreatedBy"]["displayName"]
                author_image = data["resource"]["fields"]["System.CreatedBy"]["_links"]["avatar"]["href"]
            
                time = data["resource"]["fields"]["System.CreatedDate"]
                
           
            body = {
                "content": None,
                "embeds": [
                    {
                    "title": title,
                    "description": description,
                    "url": url,
                    "color": color,
                    "author": {
                        "name": author,
                        "icon_url": author_image
                    },
                    "footer": {
                        "text": "At"
                    },
                    "timestamp": time
                    }
                ],
                "username": "Azure Devops",
                "attachments": []
            }
            
            return self.discord_api.post_webhook(body)
                
        except KeyError as e:
            return ({"error": Message.KEY_ERROR_MESSAGE.value.format(e.args[0].upper())}), 400
