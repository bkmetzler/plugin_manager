import asyncio
from pathlib import Path

from classes.models.base import BasePlugin
from classes.models.chat_message import ChatMessage
from classes.models.constants import ResponseType
from classes.plugin_manager import PluginManager


async def main():
    cm = ChatMessage(
        type=ResponseType.chat,
        sender="SENDER_ID",
        content="Message from sender"
    ).model_dump()

    pm = PluginManager(Path("classes/models/"))
    print(pm.list())
    # cht = pm.get(ResponseType.chat)

    print()


if __name__ == "__main__":
    asyncio.run(main())