import logging
from asyncio import StreamWriter
from logging import getLogger

logger = getLogger(__name__)


def log_event(writer: StreamWriter, log: str, level: int = logging.INFO):
    logger.log(level, log)
    writer(
        {
            "event": "log",
            "log": log,
            "level": logging.getLevelName(level),
        }
    )
