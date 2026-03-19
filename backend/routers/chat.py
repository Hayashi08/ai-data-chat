from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services import openai_service, snowflake_service

router = APIRouter(prefix="/api")


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    schema = snowflake_service.get_schema_info()
    sql = openai_service.generate_sql(request.message, schema)
    results = snowflake_service.execute_query(sql)

    return StreamingResponse(
        openai_service.generate_answer(request.message, sql, results),
        media_type="text/event-stream",
    )
