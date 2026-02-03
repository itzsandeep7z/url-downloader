from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

from app.downloader import download_media

app = FastAPI(
    title="Universal Downloader API",
    description="Download MP4 / MP3 / Images from any platform",
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
    file_path = os.path.join("downloads", uid, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        filename=filename,
        media_type="application/octet-stream"
    )
