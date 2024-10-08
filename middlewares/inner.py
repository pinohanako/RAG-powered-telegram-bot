import logging
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)

class TriggerEventMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Entered %s, event type: %s',
            __class__.__name__,
            event.__class__.__name__)
   
        result = await handler(event, data)
        return result

class CallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Entered %s, event type: %s',
            __class__.__name__,
            event.__class__.__name__
        )
        result = await handler(event, data)
        return result

class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        logger.debug(
            'Entered %s, event type: %s',
            __class__.__name__,
            event.__class__.__name__
        )
        result = await handler(event, data)
        return result