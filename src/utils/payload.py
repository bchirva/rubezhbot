import json

from typing import Any

def payload_value(payload: str | None, key: str) -> Any | None :
    if payload is None:
        return None

    try:
        payload_json = json.loads(payload)
        return payload_json[key]
    except ValueError:
        return None

