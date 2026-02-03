import os, uuid, shutil, threading, time
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp

app = FastAPI(title="HUNTER Downloader")

BASE_DIR = "downloads"
os.makedirs(BASE_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def auto_cleanup(path, delay=600):
    def clean():
        time.sleep(delay)
        shutil.rmtree(path, ignore_errors=True)
    threading.Thread(target=clean, daemon=True).start()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/download")
def download(url: str = Form(...)):
    uid = str(uuid.uuid4())
    out_dir = f"{BASE_DIR}/{uid}"
    os.makedirs(out_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{out_dir}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
        "merge_output_format": "mp4",
        "writethumbnail": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    files = []
    for f in os.listdir(out_dir):
        files.append(f"/api/file/{uid}/{f}")

    auto_cleanup(out_dir)

    return {
        "status": "success",
        "title": info.get("title"),
        "files": files,
        "dev": "@xoxhunterxd"
    }


@app.get("/api/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = f"{BASE_DIR}/{uid}/{filename}"
    return FileResponse(path, filename=filename)
