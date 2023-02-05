# EroEroBot

## 环境要求

虽然 `EroEroBot` 的主要依赖 [`Ariadne`](https://github.com/GraiaProject/Ariadne) 框架目前支持 Python 3.8+，但是 `EroEroBot` 使用 Python 3.9 开发，所以请使用 Python 3.9 或更高版本运行本项目。

### 下载 Python

[Download Python | Python.org](https://www.python.org/downloads/)

### 安装 Python

[在类 Unix 环境下使用 Python](https://docs.python.org/zh-cn/3/using/unix.html)

[在 Windows 上使用 Python](https://docs.python.org/zh-cn/3/using/windows.html)

### 查看 Python 版本

```bash
python3 -V
```

> Windows 系统下请使用`python`代替`python3`，下面其他命令也是。

## 配置 Mirai API HTTP

[Mirai API HTTP 安装 - Graia 官方文档](https://graia.cn/ariadne/appendix/mah-install/)

## 安装 PDM（推荐）

**EroEroBot** 使用 [**PDM**](https://pdm.fming.dev/latest/) 来管理项目

### 通过 `install-pdm.py` 安装（推荐）

```bash
# Linux / macOS
curl -sSL https://ghproxy.com/raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```

```powershell
# Windows PowerShell
(Invoke-WebRequest -Uri https://ghproxy.com/raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```

其他安装方式参见：<https://pdm.fming.dev/latest/#installation>

## 下载项目

```bash
git clone https://github.com/Graiax-Community/EroEroBot.git
cd EroEroBot
```

## 创建虚拟环境并安装依赖

```bash
pdm install

# # 如果没有安装 PDM：
# python3 -m venv .venv
#
# # Linux / macOS
# source .venv/bin/activate
# # Windows
# .venv\Scripts\Activate.ps1
#
# pip install -r requirements.txt
```

## 启动

以下两条命令任选一条执行。
`main-base.py` 对应文档中的前两章（没有使用 Saya），`main-saya.py` 对应文档第三章及之后的章节（使用 [Saya](https://graiax.cn/guide/saya.html)）

```bash
pdm run main-base.py
# #如果没有安装 PDM：
# python3 main-base.py

pdm run main-saya.py
# #如果没有安装 PDM：
# python3 main-saya.py
```

## 让 EroEroBot 保持在后台运行

### Windows / macOS

~~不会吧不会吧，不会有人连窗口最小化都不会吧~~

### Linux

#### 安装 screen

```bash
# CentOS 等 RPM 系
sudo yum install repl-release
sudo yum install screen

# Ubuntu 等 dpkg 系
sudo apt update
sudo apt install screen
```

#### 使用 screen

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
