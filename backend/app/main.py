"""App factory. Backend is loopback-only by default; LAN mode refuses to start (no access control
exists yet). docs/openapi endpoints are disabled. The research package is never registered."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import ConfigError, Settings, load_settings, validate_settings
from app.errors import ErrorCode, envelope
from app.routers import health, pairing
from app.security.middleware import SecurityMiddleware
from app.security.tokens import DenyAllValidator, TokenValidator


def _rid(request: Request) -> str:
    return str(request.scope.get("state", {}).get("request_id", ""))


def create_app(
    settings: Settings | None = None, validator: TokenValidator | None = None
) -> FastAPI:
    settings = settings or load_settings()
    validator = validator or DenyAllValidator()
    validate_settings(settings, access_control_ready=validator.production_ready)

    app = FastAPI(title="TubeSomali backend", docs_url=None, redoc_url=None, openapi_url=None)
    app.include_router(health.router)
    app.include_router(pairing.router)

    @app.exception_handler(StarletteHTTPException)
    async def _http_exc(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = ErrorCode.NOT_FOUND if exc.status_code == 404 else ErrorCode.INTERNAL_ERROR
        return JSONResponse(envelope(code, "Request failed.", _rid(request)), exc.status_code)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        # Never echo exception text (could contain user content).
        return JSONResponse(
            envelope(ErrorCode.INTERNAL_ERROR, "Internal error.", _rid(request)), 500
        )

    app.add_middleware(
        SecurityMiddleware,
        validator=validator,
        allowed_hosts=settings.allowed_hosts,
        allowed_origins=settings.allowed_origins,
    )
    return app


def run() -> None:
    """Entry point. Validates configuration BEFORE importing/starting the server."""
    try:
        settings = load_settings()
        app = create_app(settings)
    except ConfigError as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port, log_level="warning")
