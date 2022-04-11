## 如何部署 EroEroBot

### 1. 环境要求

虽然 `EroEroBot` 所依赖的 [`Ariadne`](https://github.com/GraiaProject/Ariadne) 框架目前要求的 Python 版本为 >=3.8

但 `EroEroBot` 仍然建议你使用 Python 3.9 版本进行开发

> 使用 Python 3.8 可能会存在一些未被发现的 Bug  
> 而使用 Python 3.10 则可能会存在一些第三方库仍未支持的情况

### 2. 配置 Mirai

请参阅[Ariadne官方文档关于mah的配置方法](https://graia.readthedocs.io/appendix/mah-install/)

### 3. 安装 Poetry

> 注1：假设你不想用 `Poetry`，你可直接跳过  
> 注2：此处假设你已在你的计算机或服务器上安装好 Python 3.9 / 3.10

`EroEroBot` 使用 `Poetry` 来管理项目依赖关系

安装步骤清参阅文档：<https://graiax.cn/before/Q&A.html#_6-5-poetry-%E7%9A%84%E5%AE%89%E8%A3%85>

### 4. 克隆 EroEroBot 到本地并进入项目目录中

> 你也可以不克隆而是从 Releases 中下载预发布模板（但不带任何功能）

```bash
git clone https://github.com/Graiax-Community/EroEroBot.git
cd EroEroBot
```

### 5. 创建虚拟环境并安装依赖

> 此处假设你所使用的 Python 版本为 3.9

```bash
poetry env use 3.9
poetry install
```

### 6. 启动 EroEroBot

请不要将以下命令写入 `*.sh`、`*.bat`、`*.cmd`、`*.ps1` 等脚本中使用

以下两条命令任选一条执行，`main-base.py` 对应文档中的前两章（即没有使用 Saya），
`main-saya.py` 则对应文档第三章及之后的章节（即使用 Saya）

> 有关 Saya 是什么请自行查阅文档：<https://graiax.cn/guide/saya.html>

```bash
poetry run python main-base.py
poetry run python main-saya.py
```

## 让 EroEroBot 保持在后台运行

### Windows / macOS

~~不会吧不会吧，不会有人连最小化都不会吧~~

## Linux

### 安装 screen

#### CentOS 等 RPM 系

```bash
sudo yum install repl-release
sudo yum install screen
```

#### Ubuntu 等 dpkg 系

```bash
sudo apt update
sudo apt install screen
```

### 使用 screen

1. 创建一个 screen

   ```bash
   screen -S eroerobot
   ```

2. 将 screen 放到后台

  > 在 screen 内先按下 `ctrl + a` 组合键，再按下 `d` 键

3. 将后台的 screen 调出来

   ```bash
   screen -x eroerobot  # 回到名为 eroerobot 的 screen
   screen -x  # 回到最近用过的 screen
   screen -r  # 回到最近用过的 screen
   ```
