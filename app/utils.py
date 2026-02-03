import os
import time
import shutil

def cleanup_old_downloads(base_dir: str, max_age_seconds: int = 3600):
    """
    Deletes download folders older than max_age_seconds
    Fly.io safe (no cron, no background tasks)
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


def find_files(folder):
    video = audio = image = None

    for f in os.listdir(folder):
        lf = f.lower()
        if lf.endswith(".mp4"):
            video = f
        elif lf.endswith(".mp3"):
            audio = f
        elif lf.endswith((".jpg", ".png", ".webp")):
            image = f

    return video, audio, image