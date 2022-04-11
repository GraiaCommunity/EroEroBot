import asyncio
from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.twilight import Twilight
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[Twilight.from_command("来张涩图并撤回")],
    )
)
async def recall(app: Ariadne, group: Group, message: MessageChain):
    bot_message = await app.sendGroupMessage(group, MessageChain.create(Image(path=Path("data", "imgs", "graiax.png"))))
    await asyncio.sleep(120)
    await app.recallMessage(bot_message)
