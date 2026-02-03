import yt_dlp
import os
import uuid
import shutil
import threading
import time

BASE_DIR = "downloads"


def auto_cleanup(path, delay=600):
    def clean():
        time.sleep(delay)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
    threading.Thread(target=clean, daemon=True).start()


def download_media(url: str, base_url: str):
    uid = str(uuid.uuid4())
    output_dir = os.path.join(BASE_DIR, uid)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,

        # ✅ ALWAYS DOWNLOAD A SINGLE MP4 (WORKS FOR IG/YT/X/FB)
        "format": "best[ext=mp4]/best",

        # ✅ KEEP VIDEO FILE
        "keepvideo": True,

        # ✅ WRITE IMAGE
        "writethumbnail": True,

        # ✅ EXTRACT MP3 *FROM MP4* (VIDEO WILL NOT BE DELETED)
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = []
    for f in os.listdir(output_dir):
        files.append(f"{base_url}/api/download/file/{uid}/{f}")

    auto_cleanup(output_dir)

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor"),
        "files": files,
        "dev": "@xoxhunterxd"
    }
