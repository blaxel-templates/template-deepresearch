from blaxel.telemetry.span import SpanManager
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from agent import agent
from inputs import DeepSearchInput

router = APIRouter()


@router.post("/")
async def handle_request(request: DeepSearchInput):
    with SpanManager("blaxel-langchain-deepresearch").create_active_span(
        "agent-request", {}
    ):
        return StreamingResponse(agent(request), media_type="text/event-stream")
