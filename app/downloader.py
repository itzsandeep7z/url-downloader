import yt_dlp
import os
import uuid
import shutil
import threading
import time
import zipfile

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

        # ✅ ONE MP4 (WORKS EVERYWHERE)
        "format": "best[ext=mp4]/best",

        "keepvideo": True,
        "writethumbnail": True,

        # ✅ MP3 FROM MP4
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

    files = os.listdir(output_dir)

    # 🔥 CREATE ZIP ALWAYS
    zip_name = "all.zip"
    zip_path = os.path.join(output_dir, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            zipf.write(os.path.join(output_dir, f), f)

    auto_cleanup(output_dir)

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor"),
        "files": [
            f"{base_url}/api/download/file/{uid}/{f}"
            for f in files
        ],
        "zip": f"{base_url}/api/download/file/{uid}/{zip_name}",
        "dev": "@xoxhunterxd"
    }
