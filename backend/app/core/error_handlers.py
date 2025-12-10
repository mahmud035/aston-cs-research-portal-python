from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError

async def http_error_handler(request: Request, exc: HTTPException):
    """
    Handles HTTPException raised in controllers, returning standardized JSON response.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "success": False,
            "message": exc.detail,
            "data": None,
        },
    )

async def mongo_error_handler(request: Request, exc: PyMongoError):
    """
    Handles generic PyMongo/MongoDB driver errors, avoid leaking internals.
    """
    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "success": False,
            "message": "Database error",
            "data": None,
        },
    )
