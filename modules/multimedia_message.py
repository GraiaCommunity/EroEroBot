# -*- coding: utf-8 -*-

from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Voice
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from graiax import silkcoder

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def img(app: Ariadne, group: Group, message: MessageChain):
    if message.display.strip() != "来张涩图":
        return
    await app.send_message(group, MessageChain(Image(path=Path("data", "imgs", "graiax.png"))))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def voice(app: Ariadne, group: Group, message: MessageChain):
    if message.display.strip() != "要骂骂":
        return
    voice_bytes = await silkcoder.async_encode(Path("data", "voices", "hentai.mp3"))
    await app.send_message(group, MessageChain(Voice(data_bytes=voice_bytes)))
