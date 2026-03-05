import os, uvicorn, json, sys, logging, subprocess, tempfile, uuid
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("mcp-d2")

# Configuration - CHANGE THESE VALUES
OUTPUT_DIR = "/diagrams"
BASE_URL = "https://your-domain.com/diagrams"  # Change to your domain

TOOLS = [
    {
        "name": "d2_render",
        "description": "D2 diagram rendering with multiple layout engines (elk/tala/dagre) and themes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "D2 diagram code"},
                "layout": {"type": "string", "description": "Layout engine: elk, tala, dagre", "default": "elk"},
                "theme": {"type": "string", "description": "Theme ID (0-200)", "default": "0"}
            },
            "required": ["code"]
        }
    }
]

async def handle_rpc(request):
    if request.method == "OPTIONS":
        return JSONResponse({})
    if request.method == "GET":
        return JSONResponse({"status": "mcp-d2-online", "tools": len(TOOLS)})

    try:
        raw = await request.body()
        p = json.loads(raw)
        while isinstance(p, str): 
            p = json.loads(p)
    except Exception as e:
        logger.error(f"JSON parse error: {e}")
        return JSONResponse({"error": "JSON_PARSE_ERROR"}, status_code=400)

    m, mid = p.get("method"), p.get("id", 0)

    if m and m.startswith("notifications/"):
        return JSONResponse({})

    if m == "initialize":
        return JSONResponse({"jsonrpc":"2.0","id":mid,"result":{
            "protocolVersion":"2024-11-05",
            "capabilities":{"tools":{}},
            "serverInfo":{"name":"mcp-d2","version":"1.0"}
        }})

    if m == "tools/list":
        return JSONResponse({"jsonrpc":"2.0","id":mid,"result":{"tools": TOOLS}})

    if m == "tools/call":
        nn     = p.get("params",{}).get("name")
        params = p.get("params",{}).get("arguments",{})
        res    = "No Content"
        
        try:
            if nn == "d2_render":
                code = params.get("code", "")
                layout = params.get("layout", "elk")
                theme = params.get("theme", "0")
                
                if not code:
                    res = "Error: D2 code is required"
                else:
                    # Generate unique filename
                    file_id = str(uuid.uuid4())[:12]
                    
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.d2', delete=False) as f:
                        f.write(code)
                        input_file = f.name
                    
                    svg_file = input_file.replace('.d2', '.svg')
                    png_file = os.path.join(OUTPUT_DIR, f"d2_{file_id}.png")
                    
                    try:
                        # 1. Generate SVG
                        cmd = ["d2", "--layout", layout, "--theme", theme, input_file, svg_file]
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                        
                        if result.returncode != 0:
                            res = f"D2 command failed: {result.stderr}"
                        else:
                            # 2. Convert SVG to PNG using rsvg-convert
                            convert_cmd = ["rsvg-convert", "-w", "2400", "-b", "white", "-o", png_file, svg_file]
                            convert_result = subprocess.run(convert_cmd, capture_output=True, text=True, timeout=30)
                            
                            if convert_result.returncode != 0:
                                res = f"PNG conversion failed: {convert_result.stderr}"
                            else:
                                # 3. Set file permissions
                                os.chmod(png_file, 0o644)
                                
                                # 4. Return image URL
                                image_url = f"{BASE_URL}/d2_{file_id}.png"
                                res = f"D2 Diagram (layout: {layout}, theme: {theme}):\n\n![D2 Diagram]({image_url})"
                                
                                logger.info(f"Generated diagram: {image_url}")
                        
                    finally:
                        try:
                            os.unlink(input_file)
                            if os.path.exists(svg_file):
                                os.unlink(svg_file)
                        except:
                            pass
            else:
                res = f"Unknown tool: {nn}"
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            res = f"Error: {str(e)}"
    
    return JSONResponse({"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":res}]}})

app = Starlette(routes=[Route("/", handle_rpc, methods=["GET","POST","OPTIONS"])])
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3004)
