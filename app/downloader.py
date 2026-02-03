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

        # ✅ ONE MP4 FOR ALL PLATFORMS
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

    video_url = None
    audio_url = None
    image_url = None

    for f in os.listdir(output_dir):
        lower = f.lower()
        full = f"{base_url}/api/download/file/{uid}/{f}"

        if lower.endswith(".mp4"):
            video_url = full
        elif lower.endswith(".mp3"):
            audio_url = full
        elif lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
            image_url = full

    # 🔥 ZIP ALL
    zip_name = "all.zip"
    zip_path = os.path.join(output_dir, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in os.listdir(output_dir):
            if f != zip_name:
                zipf.write(os.path.join(output_dir, f), f)

    zip_url = f"{base_url}/api/download/file/{uid}/{zip_name}"

    auto_cleanup(output_dir)

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor"),

        "video_url": video_url,
        "audio_url": audio_url,
        "image_url": image_url,
        "zip_url": zip_url,

        "dev": "@xoxhunterxd"
    }
