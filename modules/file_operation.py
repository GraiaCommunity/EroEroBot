from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent("传点涩图")],
    )
)
async def ero(app: Ariadne, group: Group):
    await app.upload_file(data=Path("data", "imgs", "secret.pdf"), target=group, name="紧身衣.pdf")
