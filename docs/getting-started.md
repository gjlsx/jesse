# 快速开始指南

## 环境配置

Jesse 需要以下技术栈：

- **Python** >= 3.10 and <= 3.13
- **pip** >= 23
- **PostgreSQL** >= 10
- **Redis** >= 5

有两种选择来配置环境：

1. **Docker 方式（推荐新手）** - [查看 Docker 指南](docker.md)
2. **本地安装** - 根据操作系统选择：
   - [Ubuntu 配置](environment-setup.md#ubuntu)
   - [macOS 配置](environment-setup.md#macos)
   - [Windows 配置](environment-setup.md#windows)

## 创建新的 Jesse 项目

你需要创建自己的 Jesse 项目来定义交易策略。

进入你要创建项目的目录并运行：

```sh
# 将 "my-bot" 改为你想要的名字
git clone https://github.com/jesse-ai/project-template my-bot
# 进入目录
cd my-bot
# 从模板创建 .env 文件
# 编辑这个文件以匹配你的环境
cp .env.example .env
```

这将创建一个包含你实际需要的文件和文件夹的新项目：

```
├── .env # 配置文件：数据库凭据、仪表板密码等
├── docker # 包含 Docker 所需配置文件的目录
├── storage # 包含日志、图表图像等的目录
└── strategies # 包含你的策略的目录
    ├── Strategy01
    │   └─ __init__.py
    └── Strategy02
        └─ __init__.py
```

## PIP 安装

如果你选择了 [Docker](docker.md) 方式，那么 Jesse 已经为你安装好了，不需要做其他事情。

如果你选择了本地安装，那么你需要通过 `pip` 安装 Jesse：

```sh
pip install jesse
```

## 使用 PIP 升级

我们在不断推送新的补丁。要升级到最新版本，运行：

```sh
pip install -U jesse
```

> **警告**：有时 pip 第一次运行上述命令时不会升级到最新版本。为了确保你运行的是最新版本，请查看 [PyPi](https://pypi.org/project/jesse/) 上的最新版本号，然后确保你在 `pip show jesse` 输出中看到该版本。

## 启动 Jesse

如果你通过 Docker 使用 Jesse，你不需要运行任何东西，这在 [Docker 文档](docker.md) 中有解释。

对于本地安装，要开始使用，（在你的 Jesse 项目内）首先确保 `POSTGRES_HOST` 和 `REDIS_HOST` 的值都设置为 `localhost`。然后运行应用程序：

```sh
jesse run
```

它会打印一个本地 URL 供你在浏览器中打开，例如：

```
INFO:     Started server process [66103]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

继续在你选择的浏览器中打开（在我的例子中）[127.0.0.1:9000](http://127.0.0.1:9000/)。如果你在服务器上运行，你可以使用服务器的 IP 地址而不是 `0.0.0.0`。

例如，如果你的服务器的 IP 地址是 `1.2.3.4`，URL 将是 [http://1.2.3.4:9000](http://1.2.3.4:9000/)。

> **提示**：如果你想更改默认的 `9000` 端口，可以通过修改项目 `.env` 文件中的 `APP_PORT` 值来实现。

## 相关链接

- [主页](https://jesse.trade/)
- [JesseGPT](https://jesse.trade/gpt)
- [博客](https://jesse.trade/blog)
- [帮助中心](https://jesse.trade/help)
- [Discord](https://jesse.trade/discord)
- [Telegram](https://t.me/jesse_trade)
- [视频教程](https://jesse.trade/youtube)
- [策略市场](https://jesse.trade/strategies)
- [更新指南](update.md)
- [Docker 部署](docker.md)
- [环境配置](environment-setup.md)
