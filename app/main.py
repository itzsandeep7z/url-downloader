from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
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
                background: radial-gradient(circle at top, #1a1a1a, #000000);
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
                text-shadow: 0 0 30px rgba(0, 255, 225, 0.25);
            }

            .tagline {
                margin-top: 15px;
                font-size: 18px;
                opacity: 0.75;
                max-width: 600px;
                line-height: 1.6;
            }

            .dev {
                margin-top: 30px;
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
                opacity: 0.4;
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
def download(url: str, request: Request):
    base_url = str(request.base_url).rstrip("/")
    try:
        return download_media(url, base_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ FILE SERVING
@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = os.path.join("downloads", uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path, filename=filename)
