from typing import Any, Optional

def send_response(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None,
    success: bool = True,
    meta: Optional[dict] = None,
) -> dict:
    """
    Unified response format — same as in Node version.
    Returns a dict ready to be returned by FastAPI.
    """
    return {
        "statusCode": status_code,
        "success": success,
        "message": message or None,
        "meta": meta or None,
        "data": data if data is not None else None,
    }
