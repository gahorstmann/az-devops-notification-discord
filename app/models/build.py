import arrow

from app.utils import Message, Color
from app.models.discord_api import DiscordApi


class Build:
    def __init__(self, settings):
        self.type = settings[0]
        self.discord_api = DiscordApi(settings[1], settings[2])
        
    def _color_switch(self, value) -> str:
        if value == "succeeded":
            return Color.GREEN.value
        elif value == "failed":
            return Color.RED.value
        elif value == "partiallySucceeded":
            return Color.YELLOW.value
        else:
            return Color.WHITE.value

    def webhook(self, data):
        try:
            result = data["resource"]["result"]
            title = f"Build: {result.replace('partially', 'partially ').capitalize()}"
            url = data["resource"]["_links"]["web"]["href"]
            author = data["resource"]["requestedFor"]["displayName"]
            author_image = data["resource"]["requestedFor"]["_links"]["avatar"]["href"]
            
            stime = arrow.get(data["resource"]["startTime"].replace("T", " ").replace("Z",""))
            ftime = arrow.get(data["resource"]["startTime"].replace("T", " ").replace("Z",""))
                        
            start_time = stime.format('YYYY-MM-DD HH:mm:ss')
            finish_time = ftime.format('YYYY-MM-DD HH:mm:ss')
            
            result = data["resource"]["result"]
            color = int(self._color_switch(result), 16)
            
            if result != "canceled":
                markdown = data["detailedMessage"]["markdown"]
            else:
                markdown = data["message"]["markdown"]
            
            description = f"""
            {markdown}
            
            * Name: {data["resource"]["definition"]["name"]}
            * Source Branch: {data["resource"]["sourceBranch"]}
            * Build Number: {data["resource"]["buildNumber"]}
            * Trigger: {data["resource"]["reason"].capitalize()}
            
            * Start Time: {start_time}
            * Finish Time: {finish_time}
           """
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
                    "timestamp": finish_time
                    }
                ],
                "username": "Azure Devops",
                "attachments": []
            }
        
            
            return self.discord_api.post_webhook(body)
                
        except KeyError as e:
            return ({"error": Message.KEY_ERROR_MESSAGE.value.format(e.args[0].upper())}), 400
