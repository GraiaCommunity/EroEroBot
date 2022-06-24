#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pkgutil

from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.saya import Saya
from graia.saya.builtins.broadcast import BroadcastBehaviour
from graia.scheduler import GraiaScheduler
from graia.scheduler.saya import GraiaSchedulerBehaviour

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
app.create(GraiaScheduler)
saya = app.create(Saya)
saya.install_behaviours(
    app.create(BroadcastBehaviour),
    app.create(GraiaSchedulerBehaviour),
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        if module_info.name.startswith("_"):
            continue
        saya.require("modules." + module_info.name)

app.launch_blocking()
