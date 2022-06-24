#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.broadcast import Broadcast

loop = asyncio.new_event_loop()
bcc = Broadcast(loop=loop)

Ariadne.config(loop=loop, broadcast=bcc)
app = Ariadne(
    connection=config(
        1919810,  # 你的机器人的 qq 号
        "GraiaxVerifyKey",  # 填入 verifyKey
        # 以下两行是你的 mirai-api-http 地址中的地址与端口
        # 默认为 "http://localhost:8080" 如果你没有改动可以省略这两行
        HttpClientConfig(host="http://11.45.1.4:19810"),
        WebsocketClientConfig(host="http://11.45.1.4:19810"),
    ),
)


@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if str(message) == "你好":
        await app.send_message(
            group,
            MessageChain(f"不要说{message.display}，来点涩图"),
        )


app.launch_blocking()
