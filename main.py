#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from datetime import datetime

from graia.ariadne.app import Ariadne
from graia.ariadne.context import adapter_ctx
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Forward, ForwardNode, Image, Voice
from graia.ariadne.message.parser.twilight import FullMatch, Sparkle, Twilight
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


# 1-3. 快速创建一个最小实例
@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    await app.sendGroupMessage(group, MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"))


# 2. 不要再戳了~
@bcc.receiver(NudgeEvent)
async def getup(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        await app.sendGroupMessage(event.group_id, MessageChain.create("别戳我，好痒"))
    else:
        await app.sendFriendMessage(event.friend_id, MessageChain.create("别戳我，好痒"))


# 3-4. Twilight的简单运用
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("涩图来")]))])
async def test(app: Ariadne, group: Group):
    await app.sendGroupMessage(group, MessageChain.create(Image(path=os.path.join("imgs", "graiax.png"))))


# 4. 关于发送语音的一些小问题
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("语音")]))])
async def hentai(app: Ariadne, group: Group):
    audio_bytes = await silkcoder.encode(os.path.join("voices", "hentai.mp3"))
    await app.sendGroupMessage(group, MessageChain.create(Voice(data_bytes=audio_bytes)))


# 5. 好大的奶
#    > 你可以自己无中生有生成消息链然后传播出去
#    > 请不要通过该方法传播谣言
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("好大的奶")]))])
async def create_forward(app: Ariadne, group: Group, member: Member):
    forward_nodes = [
        ForwardNode(
            target=member,  # 发送者的信息(Member / Friend / Stranger 都行)
            time=datetime.now(),  # 发送时间
            message=MessageChain.create(Image(path=os.path.join("imgs", "huge_milk.jpg"))),  # 要发送的消息链
        )
    ]
    member_list = await app.getMemberList(group)
    for _ in range(3):
        random_member: Member = random.choice(member_list)
        forward_nodes.append(
            ForwardNode(
                target=random_member,
                time=datetime.now(),
                message=MessageChain.create("好大的奶"),
            )
        )
    message = MessageChain.create(Forward(nodeList=forward_nodes))
    await app.sendGroupMessage(group, message)


# 6. 来点网上的涩图 -- 直接使用Ariadne自带的session进行请求
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("来点网上的涩图2")]))])
async def download_img2(app: Ariadne, group: Group):
    session = adapter_ctx.get().session
    async with session.get("https://api.ixiaowai.cn/api/api.php") as resp:
        img_bytes = await resp.read()
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=img_bytes)))


app.launch_blocking()
