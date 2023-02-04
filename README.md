# EroEroBot

GraiaX 社区文档示例 —— 大家最喜欢的涩图机器人

## 导语

众所周知，学习代码最好的办法，就是看懂文档别人的例子。
所以 `EroEroBot` 将会把 GraiaX 社区文档中的示例结合成可实际运行的机器人，以此将你们带入机器人的世界。

> 阅读 GraiaX 社区文档及 `EroEroBot` 源代码将会默认你至少学过一点点 `Python`
> 假设你连 `Python` 都不会，建议至少学点 `Python` 基础再来看

## 提示

- 本示例仓库可能会落后于文档
- 本仓库中各模块的文件名均与文档中对应章节的文件名对应（即文档链接中 `xxx.html` 的 `xxx`）
- 本仓库中不含**消息链处理器**部分的示例代码
- 本仓库包含两个 `main.py`
  > 其中，`main-base.py` 对应文档中的前两章（即没有使用 Saya），
  > `main-saya.py` 则对应文档第三章及之后的章节（即使用 Saya）
  >
  > Releases 中的 zip 包也遵循类似的命名方式
- 不会写示例的章节：
  - 快速上手（请在 Releases 中下载，不定期更新）
  - 消息链处理器
  - Console —— 后台对线
  - async_exec —— 异步画涩图
- 暂时不会写示例的章节：
  - Depend —— 不是所有人都能看涩图

## 部署

请参阅 [部署](./deploy.md)

## 文件列表

```txt
EroEroBot
├── .flake8  Flake8 代码检查工具的配置文件
├── .gitignore  Git 的配置文件之一
├── deploy.md  部署文档
├── LICENSE  开源许可证
├── main-base.py  Bot 入口（主文件）
├── main-saya.py  Bot 入口（主文件）
├── pdm.lock  PDM 的依赖锁定文件
├── pyproject.toml  本项目的配置文件（包含项目信息、PDM 的依赖及镜像源配置、Black 代码格式化工具的配置及 isort —— import 整理工具的配置）
├── README.md  说明文档
├── data/  数据目录
│   ├── imgs/  图片目录
│   └── voices/  音频文件目录
└── modules/  Saya 模块的目录
```
