from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness only. Returns no data about users, media or configuration."""
    return {"status": "ok", "phase": "1"}
