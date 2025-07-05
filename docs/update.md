# 更新升级

我们在不断发布新功能、修复错误和改进。幸运的是，升级到最新版本很容易。

## 本地安装

如果你在本地环境中使用 Jesse，升级通过 PIP 完成：

```sh
pip install -U jesse
```

> **警告**：有时 pip 第一次运行上述命令时不会升级到最新版本。为了确保你运行的是最新版本，请查看 [PyPi](https://pypi.org/project/jesse/) 上的最新版本号，然后确保你在 `pip show jesse` 输出中看到该版本。

### 检查当前版本

要检查你当前安装的 Jesse 版本：

```sh
pip show jesse
```

### 强制重新安装

如果遇到升级问题，可以强制重新安装：

```sh
pip uninstall jesse -y
pip install jesse
```

## Docker 安装

如果你通过 [Docker](docker.md) 使用 Jesse，在 `docker` 目录内运行以下命令：

```sh
# 如果容器仍在运行，先停止
docker-compose stop
# 获取最新版本
docker-compose pull
# 使用最新版本重新启动容器
docker-compose up -d
```

### 清理旧镜像

升级后，你可以清理旧的 Docker 镜像来释放磁盘空间：

```sh
# 查看所有镜像
docker images
# 删除旧的 Jesse 镜像
docker image prune
```

## 实盘交易插件

### Docker 安装的插件更新

如果你使用 [Docker](docker.md) 安装了插件，那么按上述方法更新 Jesse 本身也会更新插件。

### 本地安装的插件更新

如果你通过本地环境安装了插件，首先删除已安装的版本，然后使用以下命令重新安装：

```sh
# 删除已安装的版本
pip uninstall jesse-live -y
# 安装最新版本
jesse install-live
```

### 验证插件版本

要检查实盘交易插件是否正确安装和更新：

```sh
jesse install-live --version
```

## 更新检查

### 自动检查

Jesse 会在启动时自动检查是否有新版本可用。如果有更新，会在控制台显示提示。

### 手动检查

要手动检查是否有新版本：

```sh
# 检查 PyPi 上的最新版本
pip index versions jesse
```

## 数据库迁移

某些 Jesse 更新可能包含数据库架构变更。Jesse 会在启动时自动检查并执行必要的数据库迁移。

如果你看到以下消息，不要担心，这是正常的：

```
Checking for new database migrations...
Running migration: YYYY_MM_DD_HHMMSS_migration_name
```

### 手动迁移

如果遇到迁移问题，你可以手动运行迁移：

```sh
jesse migrate
```

### 备份数据库

在重大更新前，建议备份你的数据库：

```sh
# PostgreSQL 备份
pg_dump -U jesse_user -h localhost jesse_db > backup_$(date +%Y%m%d).sql
```

## 配置文件更新

有时新版本可能引入新的配置选项。检查你的 `.env` 文件并参考 [项目模板](https://github.com/jesse-ai/project-template) 中的最新 `.env.example` 文件，确保你有所有必要的配置项。

## 常见更新问题

### 1. 依赖冲突
如果遇到包依赖冲突：

```sh
# 创建新的虚拟环境
conda create --name jesse-new python=3.12
conda activate jesse-new
pip install jesse
```

### 2. 权限问题
在某些系统上，你可能需要管理员权限：

```sh
# Windows (以管理员身份运行 PowerShell)
pip install -U jesse

# Linux/macOS
sudo pip install -U jesse
```

### 3. 网络问题
如果下载失败，尝试使用不同的包索引：

```sh
pip install -U jesse -i https://pypi.org/simple/
```

## 版本历史

要查看 Jesse 的完整更新历史，请访问：

- [官方更新日志](https://docs.jesse.trade/docs/changelog)
- [GitHub Releases](https://github.com/jesse-ai/jesse/releases)
- [PyPi 版本历史](https://pypi.org/project/jesse/#history)

## 下一步

更新完成后：

1. 重新启动 Jesse
2. 检查 Web 界面是否正常工作
3. 验证你的策略是否兼容新版本
4. 查看新功能和改进的文档

如果遇到任何问题，请查看 [帮助中心](https://jesse.trade/help) 或加入 [Discord 社区](https://jesse.trade/discord) 寻求帮助。
