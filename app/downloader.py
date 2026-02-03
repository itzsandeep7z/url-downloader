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

        # 🎯 MP4 VIDEO
        "format": "bestvideo[ext=mp4]+bestaudio/best",
        "merge_output_format": "mp4",

        # 🎧 AUDIO → MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        # 🖼️ THUMB
        "writethumbnail": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = []
    for f in os.listdir(output_dir):
        full_link = f"{base_url}/api/download/file/{uid}/{f}"
        files.append(full_link)

    auto_cleanup(output_dir)

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor"),
        "files": files,
        "dev": "@xoxhunterxd"
    }
