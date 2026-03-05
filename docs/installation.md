# Installation Guide

## Prerequisites

- Docker Engine 20.10+
- Docker Compose V2
- Nginx (standalone or containerized)
- LobeHub instance running
- Domain with valid SSL certificate

## Quick Installation

### 1. Prepare Directories

```bash
mkdir -p /path/to/your/diagrams
chmod 755 /path/to/your/diagrams
```

### 2. Configure Files

Edit `docker-compose.yml`:
```yaml
volumes:
  - /path/to/your/diagrams:/diagrams  # Change this path
```

Edit `mcp-d2/server.py`:
```python
BASE_URL = "https://your-domain.com/diagrams"  # Change this
```

Edit `nginx/default.conf.example`:
```nginx
server_name your-domain.com;  # Change this
location /diagrams/ {
    alias /path/to/your/diagrams/;  # Change this
}
```

### 3. Build and Start

```bash
docker compose build
docker compose up -d
```

### 4. Verify

```bash
docker logs mcp-d2
# Should see: "Uvicorn running on http://0.0.0.0:3004"
```

### 5. Add to LobeHub

1. Open LobeHub Settings
2. Go to MCP Servers
3. Add: `http://localhost:3004` (or your server IP)

## Troubleshooting

### Container Won't Start
```bash
docker logs mcp-d2
docker compose build --no-cache
```

### Images Show as Black Blocks
Ensure rsvg-convert is installed:
```bash
docker exec mcp-d2 which rsvg-convert
```

### 404 on Diagram URLs
Check Nginx configuration and file permissions.

## Maintenance

### Clean Old Diagrams
```bash
find /path/to/diagrams/ -name "d2_*.png" -mtime +7 -delete
```
