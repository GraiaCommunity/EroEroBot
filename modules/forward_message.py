import random
from datetime import datetime
from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Forward, ForwardNode, Image
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Group, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast import ListenerSchema

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        decorators=[MatchContent("好大的奶")],
    )
)
async def create_forward(app: Ariadne, group: Group, member: Member):
    fwd_nodeList = [
        ForwardNode(
            target=member,
            time=datetime.now(),
            message=MessageChain(Image(path=Path("data", "imgs", "big_milk.jpg"))),
        )
    ]
    member_list = await app.get_member_list(group)
    for _ in range(3):
        random_member: Member = random.choice(member_list)
        fwd_nodeList.append(
            ForwardNode(
                target=random_member,
                time=datetime.now(),
                message=MessageChain("好大的奶"),
            )
        )
    message = MessageChain(Forward(nodeList=fwd_nodeList))
    await app.send_message(group, message)
