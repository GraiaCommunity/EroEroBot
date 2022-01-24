#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import os
import random
from datetime import datetime

import aiohttp
from graia.ariadne.app import Ariadne
from graia.ariadne.context import adapter_ctx
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import (
    At,
    Face,
    Forward,
    ForwardNode,
    Image,
    Source,
    Voice,
)
from graia.ariadne.message.formatter import Formatter
from graia.ariadne.message.parser.twilight import FullMatch, Sparkle, Twilight
from graia.ariadne.model import Group, Member, MiraiSession
from graia.broadcast.builtin.decorators import Depend
from graia.broadcast.exceptions import ExecutionStop
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
    async with session.get("https://i1.hdslb.com/bfs/archive/5242750857121e05146d5d5b13a47a2a6dd36e98.jpg") as resp:
        img_bytes = await resp.read()
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=img_bytes)))


# 8. 看完了吗，我撤回了
@bcc.receiver(GroupMessage, dispatchers=[Twilight.from_command("撤回")])
async def test(app: Ariadne, group: Group, source: Source):
    session = adapter_ctx.get().session
    async with session.get("https://i1.hdslb.com/bfs/archive/5242750857121e05146d5d5b13a47a2a6dd36e98.jpg") as resp:
        data = await resp.read()
    bot_msg = await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=data)))
    await asyncio.sleep(120)
    # await app.recallMessage(source)  # 通过 Source 撤回他人的消息
    # await app.recallMessage(source.id)  # 通过 Source 中的消息 ID 撤回他人的消息
    await app.recallMessage(bot_msg)  # 通过 BotMessage 撤回 bot 自己发的消息
    # await app.recallMessage(bot_msg.messageId)  # 通过 BotMessage 中的消息 ID 撤回 bot 自己发的消息


# 9. /斜眼笑
@bcc.receiver(GroupMessage, dispatchers=[Twilight.from_command("斜眼笑")])
async def test(app: Ariadne, group: Group):
    # await app.sendGroupMessage(
    #     group,
    #     MessageChain.create(
    #         "在新的一年里，祝你\n身",
    #         Face(277),
    #         "体",
    #         Face(277),
    #         "健",
    #         Face(277),
    #         "康\n万",
    #         Face(277),
    #         "事",
    #         Face(277),
    #         "如",
    #         Face(277),
    #         "意",
    #     ),
    # )
    await app.sendGroupMessage(
        group, Formatter("在新的一年里，祝你\n身{doge}体{doge}健{doge}康\n万{doge}事{doge}如{doge}意").format(doge=Face(277))
    )


# 10. 不是所有人都能看涩图 - Start
# ----------------------------------------------
# 本示例中部分代码并不能真正发挥作用，仅保证bot可以运行
# 请勿在未修改的情况下触发，若因触发该部分代码而出现错误
# 请不要发送 issue 或在其他平台询问
# ----------------------------------------------
def check_group(*groups: int):
    async def check_group_deco(app: Ariadne, group: Group):
        if group.id not in groups:
            await app.sendGroupMessage(group, MessageChain.create("对不起，该群并不能发涩图"))
            raise ExecutionStop

    return Depend(check_group_deco)


def check_member(*members: int):
    async def check_member_deco(app: Ariadne, group: Group, member: Member):
        if member.id not in members:
            await app.sendGroupMessage(group, MessageChain.create(At(member.id), "对不起，您的权限并不够"))
            raise ExecutionStop

    return Depend(check_member_deco)


def frequency(*args, **kwargs):
    return 0


def check_frequency(max_frequency: int):
    async def check_frequency_deco(app: Ariadne, group: Group, member: Member):
        if frequency(member.id) >= max_frequency:  # 频率判断，详细实现略
            await app.sendGroupMessage(group, MessageChain.create(At(member.id), "你太快了，能不能持久点"))
            raise ExecutionStop

    return Depend(check_frequency_deco)


@bcc.receiver(
    GroupMessage,
    decorators=[
        check_group(114514, 1919810),
        check_member(114514, 1919810),
        check_frequency(10),
    ],
    dispatchers=[Twilight.from_command("Depend测试")],
)
async def setu(app: Ariadne, group: Group, member: Member):
    # 此处的链接仅为示例，用于获取涩图api的限制，实际并不存在，请自行替换
    async with aiohttp.request("GET", "https://setu.example.com/limit") as r:
        is_max = (await r.json())["is_limit"]
    if is_max:
        await app.sendGroupMessage(group, MessageChain.create(At(member.id), "对不起，今天的涩图已经达到上限了哦"))
    else:
        ...  # 获取涩图并发送
        # await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=setu)))


# ----------------------------------------------
# 10. 不是所有人都能看涩图 - End

app.launch_blocking()
