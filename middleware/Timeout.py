import asyncio
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware


class TimeoutMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    timeout = 5
    try:
      response = await asyncio.wait_for(call_next(request), timeout)
    except asyncio.TimeoutError:
      return JSONResponse(
        {"error": "Request timed out"}, status_code=504
      )
    return response