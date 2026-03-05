# Architecture Documentation

## System Overview

This project implements a microservice-based solution for rendering D2 diagrams in LobeHub without modifying the frontend code.

## Design Principles

1. **Zero Frontend Invasion** - LobeHub frontend remains untouched
2. **Physical Isolation** - MCP server runs in isolated container
3. **Standard Protocols** - Uses MCP and HTTP/HTTPS

## Component Architecture

```
User Browser (LobeHub UI)
         ↓ HTTPS
    Nginx Reverse Proxy
    ├── /          → LobeChat
    └── /diagrams/ → Static Files
         ↓
    D2 MCP Server (:3004)
         ↓
    D2 → SVG → rsvg-convert → PNG
         ↓
    /diagrams/d2_xxx.png
```

## Data Flow

### 1. Diagram Generation
```
User: "Draw a diagram"
  ↓
Claude: Calls d2_render tool
  ↓
MCP Server: Receives D2 code
```

### 2. Processing Pipeline
```
D2 Code
  ↓ [D2 CLI]
SVG File
  ↓ [rsvg-convert]
PNG File
  ↓
Return URL
```

### 3. Image Delivery
```
LobeHub Frontend
  ↓ Markdown: ![](url)
Browser HTTP GET
  ↓
Nginx Static Serving
  ↓
PNG Rendered
```

## Technical Decisions

### Why rsvg-convert over ImageMagick?

ImageMagick's `convert` was producing grayscale images. rsvg-convert is specifically designed for SVG and preserves color correctly.

### Why PNG instead of SVG?

1. Universal browser compatibility
2. Consistent rendering
3. Better caching
4. No client-side processing

### Why Nginx Static Serving?

1. High performance
2. Built-in caching
3. Zero application logic
4. Easy CDN integration

## Security

- File system isolation
- Input validation
- Timeout limits (30s)
- HTTPS for external access

## Performance

- 7-day browser cache
- 2400px width (high DPI)
- Async processing
- Concurrent requests

## Monitoring

Key metrics:
- MCP server uptime
- Generation time
- Disk usage
- Cache hit rate
