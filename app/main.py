import os
import uuid
import shutil
import threading
import time

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp

# ---------------- CONFIG ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# ----------------------------------------

app = FastAPI(title="Universal Downloader API")

app.mount("/api/download/file", StaticFiles(directory=DOWNLOAD_DIR), name="files")

# ---------------- MODELS ----------------

class DownloadRequest(BaseModel):
    url: str

# ---------------- CLEANUP ----------------

def auto_cleanup(path, delay=600):
    def clean():
        time.sleep(delay)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
    threading.Thread(target=clean, daemon=True).start()

# ---------------- API ----------------

@app.post("/api/download")
def download_media(data: DownloadRequest):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(DOWNLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{job_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,

        # 🎯 FORCE MP4 VIDEO + M4A AUDIO SOURCE
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",

        # 🎯 MERGE VIDEO → MP4
        "merge_output_format": "mp4",

        # 🎯 SAVE THUMBNAIL
        "writethumbnail": True,

        # 🎯 KEEP VIDEO FILE
        "keepvideo": True,

        # 🎯 CONVERT AUDIO → MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            title = info.get("title", "download")
            platform = info.get("extractor_key", "Unknown")

    except Exception as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

    # ---------------- FILE LINKS ----------------

    files = []
    for f in os.listdir(job_dir):
        files.append(f"{BASE_URL}/api/download/file/{job_id}/{f}")

    # 🔥 AUTO DELETE AFTER 10 MIN
    auto_cleanup(job_dir, delay=600)

    return {
        "status": "success",
        "title": title,
        "platform": platform,
        "files": files,
        "dev": "@xoxhunterxd"
    }

# ---------------- ROOT ----------------

@app.get("/")
def root():
    return {"status": "running", "dev": "@xoxhunterxd"}
