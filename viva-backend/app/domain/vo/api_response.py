from typing import Optional, Union, Dict, List, Any

from pydantic import BaseModel, Field

class ApiResponse(BaseModel):
    status: int = Field(0, description="状态码")
    message: str | None = Field(None, description="消息")
    data: Optional[Union[Dict, List, Any]] = Field(None, description="数据")

def api_response(status=0, message=None, data=None):
    return ApiResponse(status=status, message=message, data=data)