#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Forward, ForwardNode, Image, Voice

# 包 graia.ariadne.message.parser.pattern 将在 Ariadne 0.5.0 标记为“弃用”
# 并在 Ariadne 0.5.2 正式移除，届时请从 graia.ariadne.message.parser.twilight 导入
from graia.ariadne.message.parser.pattern import FullMatch
from graia.ariadne.message.parser.twilight import Sparkle, Twilight
from graia.ariadne.model import Group, Member, MiraiSession
from graiax import silkcoder

app = Ariadne(
    MiraiSession(
        host="http://localhost:8080",
        verify_key="GraiaxVerifyKey",
        account=1919810,
        # 此处的内容请按照你的 MAH 配置来填写
    ),
)

bcc = app.broadcast


# 1-3.快速创建一个最小实例
@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    await app.sendGroupMessage(group, MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"))


# 2.不要再戳了~
@bcc.receiver(NudgeEvent)
async def getup(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        await app.sendGroupMessage(event.group_id, MessageChain.create("别戳我，好痒"))
    else:
        await app.sendFriendMessage(event.friend_id, MessageChain.create("别戳我，好痒"))


# 3-4.Twilight的简单运用
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("涩图来")]))])
async def test(app: Ariadne, group: Group):
    await app.sendGroupMessage(group, MessageChain.create(Image(path=os.path.join("imgs", "graiax.png"))))


# 4.关于发送语音的一些小问题
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("语音")]))])
async def hentai(app: Ariadne, group: Group):
    audio_bytes = await silkcoder.encode(os.path.join("voices", "hentai.mp3"))
    await app.sendGroupMessage(group, MessageChain.create(Voice(data_bytes=audio_bytes)))


# 5.好大的奶
#   > 你可以自己无中生有生成消息链然后传播出去
#   > 请不要通过该方法传播谣言
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("好大的奶")]))])
async def create_forward(app: Ariadne, group: Group, member: Member):
    forward_nodes = [
        ForwardNode(
            target=member.id,
            time=datetime.now(),
            name=member.name,
            message=MessageChain.create(Image(path=os.path.join("imgs", "huge_milk.jpg"))),
        )
    ]
    member_list = await app.getMemberList(group)
    for _ in range(3):
        random_member: Member = random.choice(member_list)
        forward_nodes.append(
            ForwardNode(
                target=random_member.id,
                time=datetime.now(),
                name=random_member.name,
                message=MessageChain.create("好大的奶"),
            )
        )
    message = MessageChain.create(Forward(nodeList=forward_nodes))
    await app.sendGroupMessage(group, message)


app.launch_blocking()
