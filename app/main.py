from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os

from app.downloader import download_media

app = FastAPI(
    title="Universal Downloader API",
    version="1.0"
)


# ✅ HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HUNTER</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background: radial-gradient(circle at top, #1a1a1a, #000);
                color: white;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
            }
            h1 {
                font-size: 110px;
                letter-spacing: 12px;
                margin: 0;
                font-weight: 800;
                background: linear-gradient(90deg, #00ffe1, #00aaff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(0,255,225,.25);
            }
            p {
                opacity: .75;
            }
            a {
                color: #00ffe1;
                text-decoration: none;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <h1>HUNTER</h1>
        <p>Universal Media Downloader API</p>
        <p>Developer <a href="https://t.me/xoxhunterxd" target="_blank">@xoxhunterxd</a></p>
    </body>
    </html>
    """


# ✅ DOWNLOAD API (SMART RESPONSE)
@app.get("/api/download")
def download(url: str, request: Request):
    base_url = str(request.base_url).rstrip("/")

    try:
        data = download_media(url, base_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 🔥 IF BROWSER → RETURN STYLED HTML
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return HTMLResponse(render_html_result(data))

    # 🔥 OTHERWISE → PURE JSON
    return JSONResponse(data)


# ✅ FILE SERVING
@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = os.path.join("downloads", uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)


# 🎨 HTML RENDER FUNCTION
def render_html_result(data: dict) -> str:
    buttons = ""
    for f in data["files"]:
        label = "Download"
        if f.endswith(".mp4"):
            label = "⬇ MP4 Video"
        elif f.endswith(".mp3"):
            label = "⬇ MP3 Audio"
        elif f.endswith(".jpg") or f.endswith(".png"):
            label = "⬇ Image"

        buttons += f"""
        <a href="{f}" target="_blank">{label}</a>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data["title"]}</title>
        <style>
            body {{
                background: #0f0f0f;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: #1a1a1a;
                padding: 40px;
                border-radius: 14px;
                text-align: center;
                width: 420px;
                box-shadow: 0 0 40px rgba(0,0,0,.5);
            }}
            h2 {{
                margin-bottom: 10px;
            }}
            .platform {{
                opacity: .7;
                margin-bottom: 25px;
            }}
            a {{
                display: block;
                margin: 12px 0;
                padding: 12px;
                background: linear-gradient(90deg, #00ffe1, #00aaff);
                color: black;
                font-weight: bold;
                border-radius: 8px;
                text-decoration: none;
            }}
            a:hover {{
                opacity: .85;
            }}
            .dev {{
                margin-top: 25px;
                font-size: 14px;
                opacity: .6;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>{data["title"]}</h2>
            <div class="platform">{data["platform"]}</div>
            {buttons}
            <div class="dev">Developer {data["dev"]}</div>
        </div>
    </body>
    </html>
    """
