from typing import Dict, Any


class DomainError(Exception):
    def __init__(self, message: str, body: Dict[str, Any]) -> None:
        self.message = message
        self.name = 'Domain Error'
        self.status_code = 422
        self.body = body
