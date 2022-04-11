import asyncio
from pathlib import Path
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Plain
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group, Member
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.saya import Channel, Saya
from graia.saya.builtins.broadcast import ListenerSchema

saya = Saya.current()
channel = Channel.current()
inc = InterruptControl(saya.broadcast)  # type: ignore


# ========================================================
# 方式一：创建一个类
# ========================================================


class SetuTagWaiter(Waiter.create([GroupMessage])):
    "涩图 tag 接收器"

    def __init__(self, group: Union[Group, int], member: Union[Member, int]):
        self.group = group if isinstance(group, int) else group.id
        self.member = member if isinstance(member, int) else member.id

    async def detected_event(self, group: Group, member: Member, message: MessageChain):
        if self.group == group.id and self.member == member.id:
            return message


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent("涩图来1")],
    )
)
async def ero1(app: Ariadne, group: Group, member: Member):
    await app.sendMessage(group, MessageChain.create("你想要什么 tag 的涩图"))
    try:
        ret_msg = await inc.wait(SetuTagWaiter(group, member), timeout=5)  # 强烈建议设置超时时间否则将可能会永远等待
    except asyncio.TimeoutError:
        await app.sendMessage(group, MessageChain.create("你说话了吗？"))
    else:
        await app.sendMessage(
            group,
            MessageChain.create(
                Plain("涩图 tag: " + ret_msg.asDisplay()),
                Image(data_bytes=Path("data", "imgs", "graiax.png").read_bytes()),
            ),
        )


# ========================================================
# 方式二：创建函数
# ========================================================


@channel.use(ListenerSchema(listening_events=[GroupMessage], decorators=[MatchContent("涩图来2")]))
async def ero(app: Ariadne, group: Group, member: Member):
    await app.sendMessage(group, MessageChain.create("你想要什么 tag 的涩图"))

    @Waiter.create_using_function([GroupMessage])
    async def setu_tag_waiter(g: Group, m: Member, msg: MessageChain):
        if group.id == g.id and member.id == m.id:
            return msg

    try:
        ret_msg = await inc.wait(setu_tag_waiter, timeout=5)  # 强烈建议设置超时时间否则将可能会永远等待
    except asyncio.TimeoutError:
        await app.sendMessage(group, MessageChain.create("你说话了吗？"))
    else:
        await app.sendMessage(
            group,
            MessageChain.create(
                Plain("涩图 tag: " + ret_msg.asDisplay()),
                Image(data_bytes=Path("data", "imgs", "graiax.png").read_bytes()),
            ),
        )
