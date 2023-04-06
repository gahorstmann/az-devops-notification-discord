from enum import Enum


class Message(Enum):
    JSON_SUCCESS_MESSAGE = "Data received successfully!"
    WEBHOOK_SUCCESS_MESSAGE = "Send Succeeded!"
    
    EVENT_TYPE_ERROR_MESSAGE = "eventType: {0} not found"
    JSON_ERROR_MESSAGE = "The JSON sent is invalid."
    KEY_ERROR_MESSAGE = "Not found key '{0}' in JSON Data"
    HEADER_REQUIRED_MESSAGE = "It is necessary to inform the headers discord-id and discord-token."
    
class Color(Enum):
    BLACK = "0x000000"
    GREEN = "0x57A64E"
    RED = "0xEA4335"
    BLUE = "0x4285F4"
    YELLOW = "0xFBBC05"
    WHITE = "0xFFFFFF"
    