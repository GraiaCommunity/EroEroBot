#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
第11章 东西要分类好
"""

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema

channel = Channel.current()

channel.name("Ero | Wyy")
channel.description("发送涩涩！ | 网易云时间提醒器")
channel.author("GraiaX")


# 由于下面的代码会造成令人厌烦的复读，因此默认注释
# @channel.use(ListenerSchema(listening_events=[GroupMessage]))
# async def ero(app: Ariadne, group: Group, message: MessageChain):
#     await app.sendGroupMessage(group, MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"))


@channel.use(SchedulerSchema(timers.crontabify("0 0 * * *")))
async def wyy(app: Ariadne):
    await app.sendGroupMessage(1919810, MessageChain.create("现在是网易云时间"))
