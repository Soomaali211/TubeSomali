"""Pairing placeholder. Not implemented: transport (Q11) and host (Q16) are undecided."""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.errors import ErrorCode, envelope

router = APIRouter()


@router.post("/pairing")
def pairing(request: Request) -> JSONResponse:
    rid = str(request.scope.get("state", {}).get("request_id", ""))
    body = envelope(ErrorCode.NOT_IMPLEMENTED, "Pairing is not implemented in this build.", rid)
    return JSONResponse(body, status_code=501)
