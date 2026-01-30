from fastapi import FastAPI, Query
import yt_dlp
import os
import uuid
import zipfile
import time
import shutil

app = FastAPI(title="Universal Downloader API")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# PLATFORM DETECTION (UX)
# -------------------------------------------------
def detect_platform(url: str):
    u = url.lower()

    if "youtube.com" in u or "youtu.be" in u:
        return "youtube"
    if "instagram.com" in u:
        return "instagram"
    if "tiktok.com" in u:
        return "tiktok"
    if "facebook.com" in u or "fb.watch" in u:
        return "facebook"
    if "twitter.com" in u or "x.com" in u:
        return "twitter"
    if "soundcloud.com" in u:
        return "soundcloud"

    return "unknown"


# -------------------------------------------------
# AUTO FILE CLEANUP (FLY.IO SAFE)
# -------------------------------------------------
def cleanup_old_downloads(base_dir, max_age_seconds=3600):
    """
    Deletes download folders older than 1 hour
    Prevents disk from filling on Fly.io
    """
    now = time.time()

    for folder in os.listdir(base_dir):
        path = os.path.join(base_dir, folder)

        if not os.path.isdir(path):
            continue

        try:
            if now - os.path.getmtime(path) > max_age_seconds:
                shutil.rmtree(path, ignore_errors=True)
        except Exception:
            pass


# -------------------------------------------------
# SAFE MEDIA EXTRACTOR
# -------------------------------------------------
def extract_all(entry):
    video_url = None
    audio_url = None
    image_url = None

    formats = entry.get("formats", [])

    # IMAGE POSTS (Instagram images)
    if not formats:
        image_url = (
            entry.get("display_url")
            or entry.get("thumbnail")
            or entry.get("url")
        )
        return video_url, audio_url, image_url

    for f in formats:
        # VIDEO (video + audio)
        if (
            f.get("vcodec") != "none"
            and f.get("acodec") != "none"
            and not video_url
        ):
            video_url = f.get("url")

        # AUDIO ONLY
        elif (
            f.get("vcodec") == "none"
            and f.get("acodec") != "none"
            and not audio_url
        ):
            audio_url = f.get("url")

    return video_url, audio_url, image_url


# -------------------------------------------------
# HEALTH CHECK (IMPORTANT)
# -------------------------------------------------
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "Universal Downloader API",
        "developer": "@xoxhunterxd"
    }


# -------------------------------------------------
# API ENDPOINT
# -------------------------------------------------
@app.get("/api/download")
async def download_api(
    url: str = Query(..., description="Any supported media URL"),
    playlist: bool = Query(False, description="true for playlist"),
    zip: bool = Query(False, description="true to download playlist as ZIP"),
):
    # Cleanup old files first (safe)
    cleanup_old_downloads(DOWNLOAD_DIR)

    request_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, request_id)
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        "quiet": True,
        "skip_download": not zip,
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",

        # REQUIRED FOR YOUTUBE & MOST PLATFORMS
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": False,

        # HUMAN-LIKE SPEED (NO PROXY / NO COOKIES)
        "sleep_interval": 3,
        "max_sleep_interval": 6,
        "concurrent_fragment_downloads": 1,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=zip)

    except Exception as e:
        return {
            "status": "error",
            "developer": "@xoxhunterxd",
            "detected_platform": detect_platform(url),
            "message": str(e),
        }

    # ---------------- ZIP (PLAYLIST) ----------------
    zip_file = None
    if playlist and zip and isinstance(info.get("entries"), list):
        zip_path = f"{output_path}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(output_path):
                for f in files:
                    z.write(os.path.join(root, f), f)
        zip_file = zip_path

    # ---------------- MULTI MEDIA (CAROUSEL / PLAYLIST) ----------------
    items = None
    if isinstance(info.get("entries"), list):
        items = []
        for e in info["entries"]:
            if not e:
                continue
            v, a, i = extract_all(e)
            items.append({
                "video_url": v,
                "audio_url": a,
                "image_url": i,
            })

    # ---------------- SINGLE MEDIA ------------------
    video_url, audio_url, image_url = extract_all(info)

    return {
        "status": "success",
        "developer": "@xoxhunterxd",
        "detected_platform": detect_platform(url),
        "platform": info.get("extractor_key"),
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),

        # SINGLE
        "video_url": video_url,
        "audio_url": audio_url,
        "image_url": image_url,

        # MULTI
        "items": items,

        # ZIP
        "zip_file": zip_file,
            }
