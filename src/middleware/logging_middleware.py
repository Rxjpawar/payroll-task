import time
import json
from fastapi import Request
from jose import jwt, JWTError
from src.models.logs import Log
from src.core.config import settings
from starlette.responses import Response
from src.database.db import SessionLocal
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # extrxtract user_id from jwt
        user_id = None
        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM]
                )
                user_id = payload.get("user_id")
            except JWTError:
                pass

        # ccapture request body (ai endpoints only)
        request_body = None
        request_query = None

        if request.url.path.startswith("/ai"):
            body_bytes = await request.body()
            if body_bytes:
                request_body = body_bytes.decode("utf-8")
                try:
                    request_json = json.loads(request_body)
                    request_query = request_json.get("query")
                except:
                    pass

        # continue request
        response = await call_next(request)

        process_time = time.time() - start_time

        # captureing response body -ai resp-
        ai_response = None

        if request.url.path.startswith("/ai"):
            response_body = b""

            async for chunk in response.body_iterator:
                response_body += chunk

            # extract ai response safely
            try:
                response_json = json.loads(response_body.decode())
                ai_response = response_json.get("response")
            except:
                ai_response = None

            # this is v imp: rebuild response correctly
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )

        #  storing th log in DB
        try:
            db = SessionLocal()

            log = Log(
                user_id=user_id,
                endpoint=request.url.path,
                response_time=process_time,
                ai_response=ai_response,
                request_query=request_query
            )

            db.add(log)
            db.commit()
            db.close()

        except Exception as e:
            # prevent mdlw crash
            print("Logging failed:", str(e))

        return response