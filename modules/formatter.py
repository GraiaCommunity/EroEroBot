# -*- coding: utf-8 -*-

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.element import Face
from graia.ariadne.message.formatter import Formatter
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight.from_command("滑稽")],
    )
)
async def recall(app: Ariadne, group: Group):
    await app.send_group_message(
        group,
        Formatter("在新的一年里，祝你\n身{doge}体{doge}健{doge}康\n万{doge}事{doge}如{doge}意").format(doge=Face(277)),
    )
