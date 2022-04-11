from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.saya import Channel
from graia.scheduler import timers
from graia.scheduler.saya import SchedulerSchema

channel = Channel.current()

group_id = 00000000  # 要定时发送消息的群号


@channel.use(SchedulerSchema(timers.every_minute()))
async def recall(app: Ariadne):
    # await app.sendGroupMessage(group_id, MessageChain.create("我又来了"))  # 这里注释掉是因为上面所设定的群号不存在
    pass
