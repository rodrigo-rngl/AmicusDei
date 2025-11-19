from pydantic import BaseModel, Field
from typing import Literal


class QueryValidation(BaseModel):
    scope: Literal[
        "catholic_doctrine",
        "general_christian",
        "other_religion",
        "off_topic",
        "ambiguous"
    ]
    category: Literal[
        "trinity", "christology", "mary_and_saints", "sacraments", "morality",
        "grace_and_salvation", "scripture_and_tradition", "liturgy", "prayer_and_spirituality",
        "ecclesiology", "canon_law", "apologetics", "history", "other"
    ]
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: str
    action: Literal["proceed_rag", "ask_clarifying", "reject"]
