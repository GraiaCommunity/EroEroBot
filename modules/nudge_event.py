from graia.ariadne.app import Ariadne
from graia.ariadne.event.mirai import NudgeEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend, Group
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def getup(app: Ariadne, event: NudgeEvent):
    if isinstance(event.subject, Group) and event.supplicant is not None:
        await app.send_group_message(event.supplicant, MessageChain("你不要光天化日之下在这里戳我啊"))
    elif isinstance(event.subject, Friend) and event.supplicant is not None:
        await app.send_friend_message(event.supplicant, MessageChain("别戳我，好痒！"))
