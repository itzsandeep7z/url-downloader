from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.downloader import download_media
import os

app = FastAPI(
    title="Universal Downloader API",
    description="MP4 / MP3 / Image Downloader",
    version="1.0",
)

@app.get("/api/download")
def download(url: str):
    try:
        return download_media(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = os.path.join("downloads", uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)
