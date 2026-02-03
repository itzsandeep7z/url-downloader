import uuid
import os
from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles

from app.downloader import download_media
from app.utils import find_files, cleanup_old_downloads

app = FastAPI(title="Universal Downloader API")

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app.mount("/files", StaticFiles(directory=DOWNLOAD_DIR), name="files")

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/api/download")
def download(request: Request, url: str = Query(...)):
    # 🔥 AUTO CLEANUP (Fly-safe)
    cleanup_old_downloads(DOWNLOAD_DIR)

    request_id = str(uuid.uuid4())
    out_dir = os.path.join(DOWNLOAD_DIR, request_id)

    info = download_media(url, out_dir)
    video, audio, image = find_files(out_dir)

    base_url = str(request.base_url).rstrip("/")
    files_url = f"{base_url}/files/{request_id}"

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor_key"),

        "video_mp4": f"{files_url}/{video}" if video else None,
        "audio_mp3": f"{files_url}/{audio}" if audio else None,
        "image": f"{files_url}/{image}" if image else None,
    }
