from app.utils import Message, Color
from app.models.discord_api import DiscordApi


class Repository:
    def __init__(self, settings):
        self.type = settings[0]
        self.discord_api = DiscordApi(settings[1], settings[2])
        
    def _color_switch(self, value) -> str:
        if value in ["push"]:
            return Color.GREEN.value
        else:
            return Color.WHITE.value

    def _type_switch(self, value) -> str:
        if value == "git-pullrequest-comment-event":
            return "comment"
        else:
            return value
    
    def pull_request(self, type, data):    
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
                        "name": author
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

    def push(self, type, data):
        try:
            title = f"{type.capitalize()}"

            url = data["resource"]["url"]
            author = data["resource"]["pushedBy"]["displayName"]
            
            date = data["resource"]["date"]
            
            description = data["detailedMessage"]["markdown"]
            
            color = int(self._color_switch(type), 16)
                    
            body = {
                "content": None,
                "embeds": [
                    {
                    "title": title,
                    "description": description,
                    "url": url,
                    "color": color,
                    "author": {
                        "name": author
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