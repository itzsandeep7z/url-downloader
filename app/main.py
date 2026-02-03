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
                background-color: #0f0f0f;
                color: white;
                font-family: Arial, Helvetica, sans-serif;
            }
            h1 {
                font-size: 80px;
                letter-spacing: 8px;
                margin: 0;
            }
            p {
                margin-top: 20px;
                font-size: 18px;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <h1>HUNTER</h1>
        <p>Developer @xoxhunterxd</p>
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
