from app.utils import Message, Color
from app.models.discord_api import DiscordApi


class Repository:
    def __init__(self, settings):
        self.type = settings[0]
        self.discord_api = DiscordApi(settings[1], settings[2])
        
    def _color_switch(self, value) -> str:
        if value in ["completed"]:
            return Color.GREEN.value
        elif value in ["abandoned"]:
            return Color.RED.value
        elif value in ["created", "comment"]:
            return Color.BLUE.value
        elif value in ["merged", "updated"]:
            return Color.YELLOW.value
        else:
            return Color.WHITE.value

    def _type_switch(self, value) -> str:
        if value == "git-pullrequest-comment-event":
            return "comment"
        else:
            return value
    
    def webhook(self, type, data):    
        try:
            if type == "updated":
                if data["resource"]["status"] != "active":
                    pr_type = self._type_switch(data["resource"]["status"])
                else:
                    pr_type = type
            else:
                pr_type = self._type_switch(type)
            
            title = f"Pull Request: {pr_type.capitalize()}"
            
            if pr_type == "comment":
                url = data["resource"]["comment"]["_links"]["self"]["href"]
                author = data["resource"]["comment"]["author"]["displayName"]
                author_image = data["resource"]["comment"]["author"]["imageUrl"]
                date = data["resource"]["comment"]["publishedDate"]
            else:
                url = data["resource"]["url"]
                author = data["resource"]["createdBy"]["displayName"]
                author_image = data["resource"]["createdBy"]["imageUrl"]
                date = data["resource"]["creationDate"]
            
            description = data["detailedMessage"]["markdown"]
            
            if pr_type == "updated":
                color = int(self._color_switch(pr_type), 16)
            else:
                color = int(self._color_switch(pr_type), 16)
                    
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
                    "timestamp": date
                    }
                ],
                "username": "Azure Devops",
                "attachments": []
            }
        
            
            return self.discord_api.post_webhook(body)
                
        except KeyError as e:
            return ({"error": Message.KEY_ERROR_MESSAGE.value.format(e.args[0].upper())}), 400
