# D2 Diagram Integration for LobeHub

[English](#english) | [中文](#中文)

---

## English

### 🎯 Overview

A seamless integration solution that enables D2 diagram rendering in LobeHub without modifying the frontend. This project implements an MCP (Model Context Protocol) server that automatically converts D2 diagrams to PNG images and serves them via Nginx.

### ✨ Features

- 🚀 **Zero Frontend Modification** - Works with vanilla LobeHub
- 🎨 **Full D2 Support** - All D2 features including layouts (elk/tala/dagre) and themes
- 🔒 **Containerized** - Fully Dockerized deployment
- 🌐 **Production Ready** - Nginx static file serving with caching
- 📊 **High Quality** - SVG to PNG conversion using rsvg-convert

### 🏗️ Architecture

```
User Request → Claude (LLM)
         ↓
    Tool Call: d2_render
         ↓
    D2 MCP Server
         ↓
    D2 → SVG → rsvg-convert → PNG
         ↓
    Save to: /diagrams/
         ↓
    Return: https://your-domain.com/diagrams/xxx.png
         ↓
    LobeHub renders natively ✅
```

### 📋 Prerequisites

- Docker & Docker Compose V2
- Nginx (can be containerized)
- LobeHub instance
- Domain with HTTPS

### 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/MaribelHearm/d2-mcp-lobehub.git
cd d2-mcp-lobehub
```

2. **Configure Nginx**
```bash
# Add to your Nginx config
location /diagrams/ {
    alias /path/to/diagrams/;
    expires 7d;
    add_header Cache-Control "public";
    add_header Access-Control-Allow-Origin "*";
}
```

3. **Deploy MCP Server**
```bash
docker compose build
docker compose up -d
```

4. **Add MCP to LobeHub**
- Open LobeHub settings
- Add MCP server: `http://your-server:3004`

### 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Architecture Details](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📝 License

MIT License - see [LICENSE](LICENSE) file for details

### 🙏 Acknowledgments

- [D2](https://d2lang.com/) - Modern diagram scripting language
- [LobeHub](https://github.com/lobehub/lobe-chat) - Open-source ChatGPT/LLMs UI
- Built for digital sovereignty systems

---

## 中文

### 🎯 项目概述

一个无缝集成方案，使 LobeHub 能够渲染 D2 拓扑图，无需修改前端代码。本项目实现了一个 MCP（模型上下文协议）服务器，自动将 D2 图表转换为 PNG 图片并通过 Nginx 提供服务。

### ✨ 核心特性

- 🚀 **前端零侵入** - 适用于原版 LobeHub
- 🎨 **完整 D2 支持** - 支持所有 D2 特性，包括布局引擎（elk/tala/dagre）和主题
- 🔒 **容器化部署** - 完全 Docker 化
- 🌐 **生产就绪** - Nginx 静态文件服务，带缓存
- 📊 **高质量输出** - 使用 rsvg-convert 进行 SVG 到 PNG 转换

### 🏗️ 架构设计

```
用户请求 → Claude (LLM)
         ↓
    工具调用: d2_render
         ↓
    D2 MCP 服务器
         ↓
    D2 → SVG → rsvg-convert → PNG
         ↓
    保存到: /diagrams/
         ↓
    返回: https://your-domain.com/diagrams/xxx.png
         ↓
    LobeHub 原生渲染 ✅
```

### 📋 前置要求

- Docker & Docker Compose V2
- Nginx（可容器化）
- LobeHub 实例
- 带 HTTPS 的域名

### 🚀 快速开始

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/d2-mcp-lobehub.git
cd d2-mcp-lobehub
```

2. **配置 Nginx**
```bash
# 添加到 Nginx 配置
location /diagrams/ {
    alias /path/to/diagrams/;
    expires 7d;
    add_header Cache-Control "public";
    add_header Access-Control-Allow-Origin "*";
}
```

3. **部署 MCP 服务器**
```bash
docker compose build
docker compose up -d
```

4. **添加 MCP 到 LobeHub**
- 打开 LobeHub 设置
- 添加 MCP 服务器：`http://your-server:3004`

### 📖 文档

- [安装指南](docs/installation.md)
- [架构详解](docs/architecture.md)
- [故障排查](docs/troubleshooting.md)

### 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

### 📝 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

### 🙏 致谢

- [D2](https://d2lang.com/) - 现代化的图表脚本语言
- [LobeHub](https://github.com/lobehub/lobe-chat) - 开源的 ChatGPT/LLMs UI

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
