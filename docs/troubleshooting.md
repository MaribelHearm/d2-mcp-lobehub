# Troubleshooting Guide

Common issues and solutions for d2-mcp-lobehub.

## 🔍 Quick Diagnostics

```bash
# Check MCP server status
docker ps | grep mcp-d2

# View logs
docker logs mcp-d2

# Check if port 3004 is listening
netstat -tulpn | grep 3004  # Linux
netstat -ano | findstr 3004  # Windows
```

## 🐛 Common Issues

### 1. Images Show as Black Blocks or Grayscale

**Symptom**: Generated diagrams appear as black rectangles or grayscale images.

**Cause**: Using ImageMagick's `convert` instead of `rsvg-convert`.

**Solution**:
```bash
# Verify rsvg-convert is installed
docker exec mcp-d2 which rsvg-convert
# Should output: /usr/bin/rsvg-convert

# Check image metadata
docker exec mcp-d2 identify -verbose /diagrams/your-image.png | head -20
# Look for: Colorspace: sRGB (good) vs Gray (bad)
```

If using ImageMagick, rebuild with correct Dockerfile.

---

### 2. MCP Server Won't Start

**Symptom**: Container keeps restarting or exits immediately.

**Diagnosis**:
```bash
# Check logs for errors
docker logs mcp-d2

# Common errors:
# - "ModuleNotFoundError" → Missing Python dependencies
# - "Permission denied" → Volume mount issues
# - "Address already in use" → Port 3004 conflict
```

**Solutions**:

**Port conflict**:
```bash
# Find what's using port 3004
lsof -i :3004  # Linux/Mac
netstat -ano | findstr 3004  # Windows

# Kill the process or change port in docker-compose.yml
```

**Rebuild container**:
```bash
docker compose stop mcp-d2
docker compose build --no-cache mcp-d2
docker compose up -d mcp-d2
```

---

### 3. 404 Error on Diagram URLs

**Symptom**: `https://your-domain.com/diagrams/d2_xxx.png` returns 404.

**Diagnosis**:
```bash
# Check if file exists
ls -lh /path/to/diagrams/

# Check Nginx can access the directory
docker exec nginx-container ls -lh /path/to/diagrams/

# Check Nginx configuration
docker exec nginx-container nginx -T | grep -A 10 "location /diagrams"
```

**Solutions**:

**File permissions**:
```bash
chmod 755 /path/to/diagrams/
chmod 644 /path/to/diagrams/*.png
```

**Nginx configuration**:
```nginx
location /diagrams/ {
    alias /path/to/diagrams/;  # Must end with /
    expires 7d;
    add_header Cache-Control "public";
}
```

**Reload Nginx**:
```bash
# If containerized
docker exec nginx-container nginx -s reload

# If on host
sudo systemctl reload nginx
```

---

### 4. LobeHub Can't Connect to MCP Server

**Symptom**: MCP server not showing in LobeHub or connection fails.

**Diagnosis**:
```bash
# Test MCP server directly
curl http://localhost:3004
# Should return: {"status":"mcp-d2-online","tools":1}

# Check network mode
docker inspect mcp-d2 | grep NetworkMode
# Should be: "host" or proper network
```

**Solutions**:

**Firewall blocking**:
```bash
# Allow port 3004
sudo ufw allow 3004  # Ubuntu
sudo firewall-cmd --add-port=3004/tcp  # CentOS
```

**Wrong URL in LobeHub**:
- Use `http://localhost:3004` if on same machine
- Use `http://server-ip:3004` if remote
- Don't use `https://` (MCP server is HTTP only)

---

### 5. D2 Command Fails

**Symptom**: Logs show "D2 command failed" errors.

**Diagnosis**:
```bash
# Check D2 is installed
docker exec mcp-d2 which d2
# Should output: /root/.local/bin/d2

# Test D2 manually
docker exec mcp-d2 bash -c "echo 'x -> y' | d2 - /tmp/test.svg"
```

**Solutions**:

**D2 not in PATH**:
```bash
# Rebuild with correct PATH
docker compose build --no-cache mcp-d2
```

**Invalid D2 syntax**:
- Check your D2 code for syntax errors
- Test at https://play.d2lang.com/

---

### 6. Disk Space Issues

**Symptom**: Container fails or diagrams not saving.

**Diagnosis**:
```bash
# Check disk usage
df -h /path/to/diagrams/

# Count diagram files
ls /path/to/diagrams/d2_*.png | wc -l
```

**Solutions**:

**Clean old diagrams**:
```bash
# Delete diagrams older than 7 days
find /path/to/diagrams/ -name "d2_*.png" -mtime +7 -delete

# Or set up a cron job
0 2 * * * find /path/to/diagrams/ -name "d2_*.png" -mtime +7 -delete
```

---

### 7. Slow Diagram Generation

**Symptom**: Takes more than 30 seconds to generate diagrams.

**Possible causes**:
- Very complex diagrams (100+ nodes)
- Slow disk I/O
- CPU constraints

**Solutions**:

**Increase timeout**:
Edit `server.py`:
```python
# Change timeout from 30 to 60 seconds
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
```

**Optimize D2 code**:
- Reduce number of nodes
- Simplify styling
- Use simpler layout engine (dagre instead of elk)

---

### 8. Git Push Fails

**Symptom**: "fatal: unable to auto-detect email address"

**Solution**:
```bash
git config --global user.name "Your Name"
git config --global user.email "username@users.noreply.github.com"
```

**Symptom**: "Repository not found"

**Solution**:
```bash
# Check remote URL
git remote -v

# Fix if wrong
git remote set-url origin https://github.com/username/repo.git
```

---

## 🔧 Advanced Debugging

### Enable Debug Logging

Edit `server.py`:
```python
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
```

Rebuild and check logs:
```bash
docker compose build mcp-d2
docker compose up -d mcp-d2
docker logs -f mcp-d2
```

### Inspect Generated Files

```bash
# Keep SVG files for debugging
# Comment out the cleanup in server.py:
# os.unlink(svg_file)  # Comment this line

# Then inspect SVG
docker exec mcp-d2 cat /tmp/xxx.svg
```

### Test Conversion Manually

```bash
# Generate test diagram
docker exec mcp-d2 bash -c "echo 'a -> b' > /tmp/test.d2"

# Run D2
docker exec mcp-d2 d2 /tmp/test.d2 /tmp/test.svg

# Convert to PNG
docker exec mcp-d2 rsvg-convert -w 2400 -b white -o /tmp/test.png /tmp/test.svg

# Check result
docker exec mcp-d2 identify /tmp/test.png
```

---

## 📞 Getting Help

If you're still stuck:

1. **Check logs first**: `docker logs mcp-d2`
2. **Search existing issues**: https://github.com/MaribelHearm/d2-mcp-lobehub/issues
3. **Open a new issue** with:
   - Error logs
   - Your configuration (sanitized)
   - Steps to reproduce
   - System info (OS, Docker version)

---

## 🎯 Prevention Tips

1. **Regular cleanup**: Set up cron job to delete old diagrams
2. **Monitor disk space**: Keep at least 1GB free
3. **Update regularly**: Pull latest changes from GitHub
4. **Backup configuration**: Keep copies of your config files
5. **Test after updates**: Generate a test diagram after any changes
