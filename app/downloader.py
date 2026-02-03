import yt_dlp
import os
import uuid
import shutil

BASE_DIR = "downloads"

def download_media(url: str):
    uid = str(uuid.uuid4())
    output_dir = os.path.join(BASE_DIR, uid)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,

        # 🎯 MP4 video + best audio
        "format": "bestvideo[ext=mp4]+bestaudio/best",

        "merge_output_format": "mp4",

        # 🎧 Convert audio to MP3
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],

        "writethumbnail": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = []
    for f in os.listdir(output_dir):
        files.append(f"/api/download/file/{uid}/{f}")

    return {
        "status": "success",
        "title": info.get("title"),
        "platform": info.get("extractor"),
        "files": files,
        "dev": "@xoxhunterxd"
    }
