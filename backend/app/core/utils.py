from typing import Any, Optional


def send_response(
    data: Any,
    status_code: int = 200,
    message: Optional[str] = None,
    success: bool = True,
    meta: Optional[dict] = None,
) -> dict:
    """
    Unified response format.
    """
    return {
        "statusCode": status_code,
        "success": success,
        "message": message,
        "meta": meta,
        "data": data,
    }
