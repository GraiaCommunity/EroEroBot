#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import pkgutil
import random
from datetime import datetime
from os.path import abspath, dirname, join

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
from graia.scheduler import GraiaScheduler, timers
from graia.scheduler.saya import GraiaSchedulerBehaviour
from graiax import silkcoder

app = Ariadne(
    MiraiSession(
        host="http://localhost:8080",
        verify_key="GraiaxVerifyKey",
        account=1919810,
        # 此处的内容请按照你的 MAH 配置来填写
    ),
)

ROOT_PATH = abspath(dirname(__file__))  # 机器人根目录

bcc = app.broadcast
loop = app.loop
sche = GraiaScheduler(loop=loop, broadcast=bcc)


# 从第 12 章起，将使用 graia-Saya 作为插件加载框架
# 即将不同的功能分为不同的文件（模块化）
# 因此，此部分为 Saya 的初始化以及模块的加载代码
# 第 1 到 11 章部分的代码将放在此部分之后
# 在本例中，各种模块将放置于 {机器人根目录}/plugins/ 中
# 在本例中，各个模块按章节而不是按功能分开
# Saya Initialization - Start
# --------------------------------------------
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour

saya = Saya(bcc)  # 初始化 Saya
saya.install_behaviours(BroadcastBehaviour(bcc))  # 为 bcc 安装 BroadcastBehaviour
saya.install_behaviours(GraiaSchedulerBehaviour(sche))  # 为定时任务安装 GraiaSchedulerBehaviour
# --------------------------------------------
# Saya Initialization - End
# Saya Module Load - Start
# --------------------------------------------
with saya.module_context():
    for module in pkgutil.iter_modules([join(ROOT_PATH, "modules")]):
        saya.require(f"modules.{module.name}")
# --------------------------------------------
# Saya Module Load - End

# 第 1 到 11 章部分的代码从此处开始
# ========================================================================================

# 1-3. 快速创建一个最小实例
# 由于每收到一条群消息都会触发，为防止风控及骚扰，默认注释
# @bcc.receiver(GroupMessage)
# async def min_test(app: Ariadne, group: Group, message: MessageChain):
#     await app.sendGroupMessage(group, MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"))


# 2. 不要再戳了~
@bcc.receiver(NudgeEvent)
async def nudge_test(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        await app.sendGroupMessage(event.group_id, MessageChain.create("别戳我，好痒"))
    else:
        await app.sendFriendMessage(event.friend_id, MessageChain.create("别戳我，好痒"))


# 3-4. Twilight的简单运用
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("3-4涩图来")]))])
async def twilight_test(app: Ariadne, group: Group):
    await app.sendGroupMessage(group, MessageChain.create(Image(path=join(ROOT_PATH, "data", "imgs", "graiax.png"))))


# 4. 关于发送语音的一些小问题
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("4语音")]))])
async def voice_test(app: Ariadne, group: Group):
    audio_bytes = await silkcoder.encode(join(ROOT_PATH, "data", "voices", "hentai.mp3"))
    await app.sendGroupMessage(group, MessageChain.create(Voice(data_bytes=audio_bytes)))


# 5. 好大的奶
#    > 你可以自己无中生有生成消息链然后传播出去
#    > 请不要通过该方法传播谣言
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("5好大的奶")]))])
async def forward_test(app: Ariadne, group: Group, member: Member):
    forward_nodes = [
        ForwardNode(
            target=member,  # 发送者的信息(Member / Friend / Stranger 都行)
            time=datetime.now(),  # 发送时间
            message=MessageChain.create(Image(path=join(ROOT_PATH, "data", "imgs", "huge_milk.jpg"))),  # 要发送的消息链
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
@bcc.receiver(GroupMessage, dispatchers=[Twilight(Sparkle([FullMatch("6来点网上的涩图")]))])
async def download_test(app: Ariadne, group: Group):
    session = adapter_ctx.get().session
    async with session.get("https://i1.hdslb.com/bfs/archive/5242750857121e05146d5d5b13a47a2a6dd36e98.jpg") as resp:
        img_bytes = await resp.read()
    await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=img_bytes)))


# 8. 看完了吗，我撤回了
@bcc.receiver(GroupMessage, dispatchers=[Twilight.from_command("8撤回")])
async def recall_test(app: Ariadne, group: Group, source: Source):
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
@bcc.receiver(GroupMessage, dispatchers=[Twilight.from_command("9斜眼笑")])
async def format_test(app: Ariadne, group: Group):
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
# --------------------------------------------
# 本示例中部分代码并不能真正发挥作用，仅保证bot可以运行
# 请勿在未修改的情况下触发，若因触发该部分代码而出现错误
# 请不要发送 issue 或在其他平台询问
# --------------------------------------------
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
    dispatchers=[Twilight.from_command("10Depend测试")],
)
async def check_test(app: Ariadne, group: Group, member: Member):
    # 此处的链接仅为示例，用于获取涩图api的限制，实际并不存在，请自行替换
    async with aiohttp.request("GET", "https://setu.example.com/limit") as r:
        is_max = (await r.json())["is_limit"]
    if is_max:
        await app.sendGroupMessage(group, MessageChain.create(At(member.id), "对不起，今天的涩图已经达到上限了哦"))
    else:
        ...  # 获取涩图并发送
        # await app.sendGroupMessage(group, MessageChain.create(Image(data_bytes=setu)))


# --------------------------------------------
# 10. 不是所有人都能看涩图 - End

# 11-1. 哦嗨哟，欧尼酱 —— 每分钟都在群里发垃圾消息
# 为避免风控及骚扰，此部分代码默认注释掉
# @sche.schedule(timers.every_minute())
# async def every_minute_speaki_test(app: Ariadne):
#     await app.sendGroupMessage((await app.getGroupList())[0], MessageChain.create("我又来了"))

# 11-2. 哦嗨哟，欧尼酱 —— 每天7点30分30秒叫起床
@sche.schedule(timers.crontabify("30 7 * * * 30"))
async def every_minute_speaki_test(app: Ariadne):
    await app.sendGroupMessage((await app.getGroupList())[0], MessageChain.create("哦嗨哟，欧尼酱"))


# ========================================================================================
# 第 1 到 11 章部分的代码到此结束

app.launch_blocking()
