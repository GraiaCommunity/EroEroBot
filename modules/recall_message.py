# -*- coding: utf-8 -*-

import asyncio
from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent("来张涩图并撤回")],
    )
)
async def recall(app: Ariadne, group: Group):
    bot_message = await app.send_group_message(group, MessageChain(Image(path=Path("data", "imgs", "graiax.png"))))
    await asyncio.sleep(120)
    await app.recall_message(bot_message)
