from fastapi import FastAPI, Query
import yt_dlp
import os
import uuid
import zipfile

app = FastAPI(title="Universal Downloader API")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# -------------------------------------------------
# Write Instagram cookies from Railway ENV (if any)
# -------------------------------------------------
COOKIE_PATH = "/tmp/instagram_cookies.txt"

if "IG_COOKIES" in os.environ:
    with open(COOKIE_PATH, "w", encoding="utf-8") as f:
        f.write(os.environ["IG_COOKIES"])


# -------------------------------------------------
# SAFE MEDIA EXTRACTOR
# -------------------------------------------------
def extract_all(entry):
    video_url = None
    audio_url = None
    image_url = None

    formats = entry.get("formats")

    # IMAGE POSTS / NO FORMATS
    if not formats:
        image_url = (
            entry.get("display_url")
            or entry.get("url")
            or entry.get("thumbnail")
        )
        return video_url, audio_url, image_url

    # VIDEO + AUDIO
    for f in formats:
        if (
            f.get("vcodec") != "none"
            and f.get("acodec") != "none"
            and not video_url
        ):
            video_url = f.get("url")

        elif (
            f.get("vcodec") == "none"
            and f.get("acodec") != "none"
            and not audio_url
        ):
            audio_url = f.get("url")

    # IMAGE FALLBACK
    if not video_url and not audio_url:
        image_url = (
            entry.get("display_url")
            or entry.get("thumbnail")
            or entry.get("url")
        )

    return video_url, audio_url, image_url


# -------------------------------------------------
# API ENDPOINT
# -------------------------------------------------
@app.get("/api/download")
async def download_api(
    url: str = Query(..., description="Any supported media URL"),
    playlist: bool = Query(False, description="true for playlist"),
    zip: bool = Query(False, description="true to download playlist as ZIP"),
):
    request_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, request_id)
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        "quiet": True,
        "skip_download": not zip,
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",
    }

    # Always use cookies if available (Instagram stability)
    if os.path.exists(COOKIE_PATH):
        ydl_opts["cookiefile"] = COOKIE_PATH

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

    except Exception:
        return {
            "status": "error",
            "developer": "@xoxhunterxd",
            "message": "Unable to extract media from this URL",
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

    # ---------------- MULTIPLE MEDIA (CAROUSEL) -----
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
        "platform": info.get("extractor_key"),

        # SINGLE
        "video_url": video_url,
        "audio_url": audio_url,
        "image_url": image_url,

        # MULTI
        "items": items,

        # ZIP
        "zip_file": zip_file,

        # META
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
    }
# -------------------------------------------------