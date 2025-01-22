from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/submitEssay")
async def submit_essay(request: Request):
    try:
        # 现有的处理逻辑
        # ...
        pass
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})
