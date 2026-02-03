import uuid
import os
from yt_dlp import YoutubeDL

BASE_DIR = "downloads"

def download_media(url: str, base_url: str):
    uid = str(uuid.uuid4())
    out_dir = os.path.join(BASE_DIR, uid)
    os.makedirs(out_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,

        # MP4 VIDEO
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4",

        # MP3 AUDIO
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        # IMAGE
        "writethumbnail": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = []
    for f in os.listdir(out_dir):
        files.append(f"{base_url}/api/download/file/{uid}/{f}")

    return {
        "status": "success",
        "title": info.get("title"),
        "extractor": info.get("extractor"),
        "files": files,
    }