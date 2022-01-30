# EroEroBot

GraiaX 社区文档示例 —— 大家最喜欢的涩图机器人

## 导语

众所周知，学习代码最好的办法，就是看懂文档别人的例子  
所以 `EroEroBot` 将会把 GraiaX 社区文档中的示例结合成可实际运行的机器人  
以此将你们带入机器人的世界

> 阅读 GraiaX 社区文档及 `EroEroBot` 源代码将会默认你至少学过一点点 `Python`  
> 假设你连 `Python` 都不会，建议至少学点 `Python` 基础再来看

## 部署

请参阅 [部署](./deploy.md)

## 文件列表

```
EroEroBot
├── .flake8  Flake8 代码检查工具的配置文件
├── .gitignore  Git 的配置文件之一
├── deploy.md  部署文档
├── LICENSE  开源许可证
├── main.py  Bot 入口（主文件）
├── poetry.lock  Poetry 的依赖锁定文件
├── pyproject.toml  本项目的配置文件（包含项目信息、Poetry 的依赖及镜像源配置、Black 代码格式化工具的配置及 isort —— import 整理工具的配置）
├── README.md  说明文档
├── requirements.txt  依赖项（不推荐使用）
├── data/  数据目录
│   ├── imgs/  图片目录
│   └── voices/  音频文件目录
└── modules/  Saya 模块的目录
```

## `EroEroBot` 目前实现的文档中的例子

0. ~~先谈好 —— 开始之前，你需要知道的事情~~
1. 你好，来点涩图 —— 你与机器人的第一次对话
2. 别戳了 —— `Ariadne` 上各类 `Event` 的简单讲解
3. 来点涩图 —— `Twilight` 的简单运用以及 `MessageChain` 的构建
4. 八嘎 hentai 无路赛 —— 对于**多媒体消息**发送的一点补充
5. 好大的奶 —— 合并消息的构建
6. 来点网络上的涩图 —— `aiohttp` 的超简单运用
7. 来点xxx涩图 —— `Twilight` 的参数获取和 `Detectxxx` 的运用
8. 看完了吗，我撤回了 —— 异步延时和 `Ariadne` 实例的其他方法介绍
9. /斜眼笑 —— `Formatter` 的运用
10. 不是所有人都能看涩图 —— `Depend` 的简单运用
11. 准时叫你起床板砖 —— `graia-scheduler` 的使用
12. 东西要分类好 —— `graia-saya` 的使用

**截止本次 commit，文档还没写完，所以以下章节的示例均没有实现**

> 13. 请问您这次要怎么样的涩图 —— `interrupt` 的简单运用
> 14. Wow, 这个好涩 —— `Component` 的简单运用
> 15. 无内鬼，来点加密压缩包 —— 关于**文件操作**的简单实例
> 16. 加速画涩图速度 —— `cpu_bound` 的运用
