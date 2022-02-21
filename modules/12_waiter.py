#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
第12章 请问今天你想要怎么样的涩图
"""

from pathlib import Path
from typing import List, Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group, Member
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


class SetuTagWaiter(Waiter.create([GroupMessage])):
    "涩图 tag 接收器"

    def __init__(self, group: Union[Group, int], member: Union[Member, int]):
        self.group = group if isinstance(group, int) else group.id
        self.member = member if isinstance(member, int) else member.id

    async def detected_event(self, group: Group, member: Member, message: MessageChain):
        if self.group == group.id and self.member == member.id:
            return message


async def setu(tag: List[str]) -> bytes:
    # 都说了，涩图 api 可是至宝，怎么可能轻易给你
    return Path("src/dio.jpg").read_bytes()


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MatchContent("121涩图来")]))
async def ero1(app: Ariadne, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create("你想要什么 tag 的涩图"))
    inc = InterruptControl(app.broadcast)
    ret_msg = await inc.wait(SetuTagWaiter(group, member))
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=(await setu(ret_msg.split())))))


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MatchContent("122涩图来")]))
async def ero2(app: Ariadne, group: Group, member: Member):
    await app.sendGroupMessage(group, MessageChain.create("你想要什么 tag 的涩图"))

    @Waiter.create_using_function([GroupMessage])
    async def setu_tag_waiter(g: Group, m: Member, msg: MessageChain):
        if group.id == g.id and member.id == m.id:
            return msg

    inc = InterruptControl(app.broadcast)
    ret_msg = await inc.wait(setu_tag_waiter)
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=(await setu(ret_msg.split())))))
