from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
import os
from app.downloader import download_media

app = FastAPI(title="Universal Downloader API")

@app.get("/api/download")
def download(url: str, request: Request):
    base_url = str(request.base_url).rstrip("/")
    try:
        return download_media(url, base_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = os.path.join("downloads", uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)
