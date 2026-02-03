from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import threading
import time

from app.downloader import download_media

app = FastAPI()
BASE_DIR = "downloads"

@app.get("/api/download")
def download(
    request: Request,
    url: str = Query(...)
):
    base_url = str(request.base_url).rstrip("/")
    return download_media(url, base_url)

@app.get("/api/download/file/{uid}/{filename}")
def serve_file(uid: str, filename: str):
    path = os.path.join(BASE_DIR, uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404)
    return FileResponse(path, filename=filename)

# AUTO CLEANUP (30 MINUTES)
def cleanup():
    while True:
        time.sleep(1800)
        if os.path.exists(BASE_DIR):
            shutil.rmtree(BASE_DIR)
            os.makedirs(BASE_DIR)

threading.Thread(target=cleanup, daemon=True).start()