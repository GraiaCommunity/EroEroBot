#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group, MiraiSession

app = Ariadne(
    MiraiSession(
        # 以下3行请按照你的 MAH 配置来填写
        host="http://localhost:8080",  # 同 MAH 的 port
        verify_key="GraiaxVerifyKey",  # 同 MAH 配置的 verifyKey
        account=1919810,  # 机器人 QQ 账号
    ),
)
bcc = app.broadcast


@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if str(message) == "你好":
        await app.sendMessage(
            group,
            MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"),
        )


app.launch_blocking()
