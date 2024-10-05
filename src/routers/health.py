from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def health_check():
    """
    Health check endpoint just for testing.
    """
    return {"message": "pong"}
