# 环境配置

在安装 Jesse 之前，你需要准备环境。我们将介绍三个主要操作系统的配置：

- Ubuntu
- macOS
- Windows

> **提示**：如果你想使用 [Docker](docker.md)，则不需要执行这些步骤。

> **提示**：为运行 Python 应用程序提供环境的一个好习惯是建立 Python 虚拟环境。特别是当你有不同的项目，每个项目都有自己的依赖项时，你可以创建一个独立的环境，无论其他项目有什么依赖项。

## 远程服务器

如果你打算使用远程服务器，我们为你提供了分步骤的 YouTube 演示：

- [如何在 VSCode 中为算法交易设置远程开发环境](https://www.youtube.com/watch?v=hAcG8Oey4VE) 🎥
- [如何将你的 Jesse 项目部署到生产服务器进行实盘交易](https://www.youtube.com/watch?v=cUNX5FAVVYo) 🎥

## Ubuntu

🎥 **视频教程**：如果你更喜欢观看视频，这里有一个 [解释 Ubuntu 设置的录屏](https://www.youtube.com/watch?v=00RY6eL5CXw)。

### 全新安装（推荐用于新创建的服务器）

我们提供了一个 [bash 脚本](https://github.com/jesse-ai/stack-installer)，可以在运行 Ubuntu 22.04 LTS 全新安装的机器上安装所有必需的技术栈和 pip 包。

```sh
source <(curl -fsSL https://raw.githubusercontent.com/jesse-ai/stack-installer/master/ubuntu-22.04.sh)
```

### 现有安装（推荐用于桌面用户）

如果你无法进行全新安装，你可以查看我们脚本使用的命令，只执行适合你环境的命令：

#### 安装 Miniconda

前往 [Miniconda](https://www.anaconda.com/download/success/) 网站，下载适合你系统的最新版本。

进入你下载文件的目录并运行以下命令。

记住在安装过程结束时输入 "yes" 来初始化 conda。

```sh
bash {你下载的文件名}
```

要创建新环境并激活它，运行以下命令：

```sh
conda create --name jesse python=3.12
conda activate jesse
```

> **提示**：记住每次打开新终端时都需要运行 `conda activate jesse` 来激活环境。

#### 安装 PostgreSQL

要安装 PostgreSQL，运行以下命令：

```sh
sudo apt-get install postgresql postgresql-contrib
```

要创建数据库和用户，运行以下命令：

```sh
sudo -u postgres psql -c "CREATE DATABASE jesse_db;"
sudo -u postgres psql -c "CREATE USER jesse_user WITH PASSWORD 'password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE jesse_db TO jesse_user;"
sudo -u postgres psql -c "ALTER DATABASE jesse_db OWNER TO jesse_user;"
```

#### 安装 Redis

要安装 Redis，运行以下命令：

```sh
sudo apt-get install redis-server
```

> **重要**：默认情况下，`POSTGRES_HOST` 和 `REDIS_HOST` 的值设置为 `postgres` 和 `redis`，这是官方 Docker 容器的默认值。你必须将它们都更改为 `localhost`。

你的环境现在应该准备好[安装和运行](getting-started.md) Jesse 了。

## macOS

🎥 **视频教程**：如果你更喜欢观看视频，这里有一个 [解释 macOS 设置的录屏](https://youtu.be/R0uTj92wRTU)。

在 macOS 上使用 Homebrew 和 Miniconda 进行安装是很简单的。按照以下步骤设置你的环境：

### 1. 安装 Homebrew

如果你还没有安装 [Homebrew](https://brew.sh/)，运行这个命令：

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

### 2. 安装 Miniconda

Miniconda 提供独立的 Python 环境，防止与系统上其他 Python 包冲突。

对于 Apple Silicon（M1/M2/M3/M4）机器：

```sh
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

对于基于 Intel 的机器：

```sh
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh
```

初始化 conda：

```sh
source ~/miniconda3/bin/activate
conda init --all
```

### 3. 创建 Jesse 环境

使用 Python 3.12 为 Jesse 创建专用环境：

```sh
conda create --name jesse python=3.12
```

每当你使用 Jesse 时激活环境：

```sh
conda activate jesse
```

### 4. 安装必需的包

通过 Homebrew 安装基本依赖项：

```sh
brew install redis postgresql@17
```

### 5. 配置 PostgreSQL

为 Jesse 创建数据库和用户：

```sh
# 打开 PostgreSQL CLI
psql postgres
# 创建数据库
CREATE DATABASE jesse_db;
# 创建新用户
CREATE USER jesse_user WITH PASSWORD 'password';
# 设置创建的用户的权限
GRANT ALL PRIVILEGES ON DATABASE jesse_db to jesse_user;
# 将数据库的所有者设置为新用户（PostgreSQL >= 15 需要）
ALTER DATABASE jesse_db OWNER TO jesse_user;
# 退出 PostgreSQL CLI
\q
```

你的 macOS 环境现在准备好[安装和运行 Jesse](getting-started.md) 了。

## Windows

🎥 **视频教程**：如果你更喜欢观看视频，这里有一个 [解释 Windows 设置的录屏](https://youtu.be/R5aIUmOOBr8)。

### Miniconda

Miniconda 提供独立的 Python 环境，防止与系统上其他 Python 包冲突。

在 PowerShell 中使用这些命令下载并安装 Miniconda：

```sh
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe -o .\miniconda.exe
start /wait "" .\miniconda.exe /S
del .\miniconda.exe
```

使用 Python 3.12 为 Jesse 创建专用环境：

```sh
conda create --name jesse python=3.12
```

每当你使用 Jesse 时激活环境：

```sh
conda activate jesse
```

记住，你需要在打开的每个新 PowerShell 窗口中运行 `conda activate jesse` 命令，然后才能运行任何 Jesse 或 Python 命令。

### Redis

坏消息是没有 Windows 版本的 Redis。好消息是：我们可以借助虚拟机（VM）或 Windows 子系统来安装 Redis。这里我们将在 Windows 子系统上使用 Linux：

在安装任何适用于 WSL 的 Linux 发行版之前，你必须确保启用了"Windows Subsystem for Linux"可选功能：

以管理员身份打开 PowerShell（在 Windows 搜索中搜索"PowerShell" > 右键单击 > "以管理员身份运行"）并输入：

```sh
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```

在提示时重启计算机。

现在从 [Microsoft Store](http://microsoft.com/store) 下载并安装 [Ubuntu 20.04](https://www.microsoft.com/en-us/store/p/ubuntu-2004-lts/9n6svws3rx71)。

启动 Ubuntu，你将被提示为 Ubuntu 选择用户名和密码。

之后安装 Redis（你将被要求输入你刚设置的密码）：

```sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis-server
redis-cli -v
```

你应该会看到类似这样的内容：`redis-cli X.X.X`

这将启动服务器。之后你可以关闭窗口：

```sh
redis-server
```

但你需要在每次系统重启后通过在 Ubuntu 终端中运行 redis-server 命令来启动 Redis 服务器。

另一个替代方案是 [Memurai](https://www.memurai.com/) - 不过免费版本每 10 天需要重启一次。

### PostgreSQL

[下载](https://www.postgresql.org/download/windows) 并安装大于 `11.2` 版本，匹配你的系统类型（Windows `x86-64` 或 `x86-32`）。

> **警告**：确保保存你为超级用户设置的密码。你可以取消选择组件 `pgAdmin` 和 `Stack Builder`。你可以保留其他设置不变。

现在将 PostgreSQL 添加到你的 `PATH`。要编辑你的 `PATH` 变量，使用 Windows 搜索并搜索 `environment`。单击 `Edit environment variables for your account`。在用户部分搜索 `PATH` 变量。选择它并单击 `Edit`。现在单击 `Browse` 并找到你的 PostgreSQL 安装文件夹。选择 `bin` 文件夹并保存所有内容。添加的路径应该类似于 `C:\Program Files\PostgreSQL\12\bin`。

现在打开 CMD 通过执行以下命令为 Jesse 创建数据库：

```sh
# 切换到 postgres 用户。你将被要求输入密码
psql -U postgres
# 创建数据库
CREATE DATABASE jesse_db;
# 创建新用户
CREATE USER jesse_user WITH PASSWORD 'password';
# 设置创建的用户的权限
GRANT ALL PRIVILEGES ON DATABASE jesse_db to jesse_user;
# 将数据库的所有者设置为新用户（PostgreSQL >= 15 需要）
ALTER DATABASE jesse_db OWNER TO jesse_user;
# 退出 PostgreSQL CLI
\q
```

### Cython

运行：

```sh
pip install cython
```

就这样！你现在应该能够[安装和运行](getting-started.md) Jesse 了。
