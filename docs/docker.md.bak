# Docker 部署

所有 Docker 所需的配置文件都随 [新的 Jesse 项目](getting-started.md#创建新的-jesse-项目) 一起提供。

🎥 **视频教程**：如果你是视觉学习者，可以观看 [这个 YouTube 视频](https://youtu.be/W8Hh56HJ-0I)，它介绍了如何使用 Docker 运行 Jesse。

该视频还介绍了在 VSCode 中启用代码智能感知，这是快速开发的好工具。

**Kubernetes**：如果你有兴趣使用 Kubernetes 和 Helm 而不是 Docker 来运行 Jesse，请查看社区维护的仓库 [jesse-chart](https://github.com/TrianaLab/jesse-chart)。

## 安装 Docker

如果你使用 macOS 或 Windows，我建议安装 [Docker for Desktop](https://www.docker.com/products/docker-desktop) 应用程序（如果你还没有安装的话）。如果你使用 Ubuntu，以下是步骤：

```sh
# 安装 docker
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
# 安装 docker-compose 
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose
```

## 启动容器

如果你还没有[创建 Jesse 项目](getting-started.md#创建新的-jesse-项目)，确保先创建一个。接下来我们可以启动容器。

所有 Docker 的配置文件都在你项目的 `docker` 目录中。如果没有，只需从 [这个仓库](https://github.com/jesse-ai/project-template) 复制它。

然后在终端中确保你在项目根目录，打开 `docker` 目录并运行 docker-compose 命令：

```sh
# 打开 `docker` 目录
cd docker
# 运行时不使用 "-d" 标志可以看到输出
docker-compose up -d
```

第一次执行时，你需要等待直到镜像下载完成。这可能需要几分钟。但下次会快很多，不过仍然可能需要超过 10 秒来启动所有服务。

就这样！现在在你的浏览器中打开 [localhost:9000](http://localhost:9000/) 来查看仪表板。

## 停止容器

要停止容器，如果你使用 `-d` 标志启动它们，你只需运行以下命令：

```sh
docker-compose stop
```

如果你没有使用 `-d` 标志（这样你可以在终端中看到输出），你可以通过在键盘上按 `Ctrl` + `c` 来停止容器。

## 更改端口

如果你想更改默认的 `9000` 端口，可以通过修改项目 `.env` 文件中的 `APP_PORT` 值来实现。

## 跨实例共享数据库

你可以通过共享 postgres 容器的卷来使用相同的数据库。只需在你创建的新实例的 `docker-compose.yml` 中添加 `external: true`，如下所示。这告诉 docker 不要创建新卷，而是使用外部现有的卷。

```yaml
volumes:
  postgres-data:
    external: true
```

## Docker Compose 文件说明

Jesse 项目包含的 `docker-compose.yml` 文件定义了以下服务：

### Jesse 服务
- **镜像**：`salehmir/jesse:latest`
- **端口**：
  - `9000:9000` - Web 仪表板
  - `8888:8888` - Jupyter Notebook（可选）
- **依赖**：PostgreSQL 和 Redis
- **卷挂载**：将项目目录挂载到容器的 `/home` 目录

### PostgreSQL 数据库
- **镜像**：`postgres:14-alpine`
- **环境变量**：
  - `POSTGRES_USER=jesse_user`
  - `POSTGRES_PASSWORD=password`
  - `POSTGRES_DB=jesse_db`
- **数据持久化**：使用 Docker 卷存储数据

### Redis 缓存
- **镜像**：`redis:6-alpine`
- **配置**：禁用持久化以提高性能

## 常见问题

### 1. 容器启动失败
- 确保 Docker 正在运行
- 检查端口 9000 是否被其他应用占用
- 查看容器日志：`docker-compose logs`

### 2. 无法访问 Web 界面
- 确认容器正在运行：`docker-compose ps`
- 检查防火墙设置
- 尝试使用 `127.0.0.1:9000` 而不是 `localhost:9000`

### 3. 数据库连接问题
- 检查 `.env` 文件中的数据库配置
- 确保数据库容器正在运行
- 查看数据库日志：`docker-compose logs postgres`

### 4. 更新 Jesse
要更新到最新版本的 Jesse：

```sh
# 停止容器
docker-compose stop
# 拉取最新镜像
docker-compose pull
# 重新启动容器
docker-compose up -d
```
