from typing import Dict, Any


class ServerError(Exception):
    def __init__(self, message: str, body: Dict[str, Any]) -> None:
        self.message = message
        self.name = 'Server Error'
        self.status_code = 500
        self.body = body
