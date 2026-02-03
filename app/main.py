from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pathlib import Path
import os

from app.downloader import download_media

BASE_DIR = Path("downloads")

app = FastAPI(
    title="Universal Downloader API",
    version="1.1",
    description="Platform-independent media downloader API"
)

# ✅ HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                font-family: 'Segoe UI', system-ui, sans-serif;
                text-align: center;
                overflow: hidden;
            }

            h1 {
                font-size: clamp(64px, 10vw, 110px);
                letter-spacing: 12px;
                margin: 0;
                font-weight: 800;
                background: linear-gradient(90deg, #00ffe1, #00aaff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(0, 255, 225, 0.25);
            }

            .tagline {
                margin-top: 20px;
                font-size: 18px;
                opacity: 0.75;
                max-width: 640px;
                line-height: 1.6;
            }

            .dev {
                margin-top: 35px;
                font-size: 20px;
            }

            .dev a {
                color: #00ffe1;
                text-decoration: none;
                font-weight: 600;
            }

            .dev a:hover {
                text-decoration: underline;
            }

            .footer {
                position: absolute;
                bottom: 20px;
                font-size: 14px;
                opacity: 0.35;
            }
        </style>
    </head>
    <body>
        <h1>HUNTER</h1>

        <div class="tagline">
            Universal media extraction API.<br>
            Download videos, audio, images — fast, clean, and platform-independent.
            <br><br>
            Built for developers, automation, and content tools.
        </div>

        <div class="dev">
            Developer
            <a href="https://t.me/xoxhunterxd" target="_blank">@xoxhunterxd</a>
        </div>

        <div class="footer">
            © HUNTER API
        </div>
    </body>
    </html>
    """


# ✅ DOWNLOAD API
@app.get("/api/download")
def download(
    url: str = Query(..., min_length=10, description="Media URL"),
    request: Request = None
):
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    base_url = str(request.base_url).rstrip("/")

    try:
        return download_media(url, base_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Download failed", "detail": str(e)}
        )


# ✅ FILE SERVING
@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    file_path = BASE_DIR / uid / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
