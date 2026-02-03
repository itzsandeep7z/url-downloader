from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import os

from app.downloader import download_media

app = FastAPI(
    title="Universal Downloader API",
    version="1.0"
)

# ================= HOME PAGE =================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HUNTER</title>
        <style>
            body {
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background: radial-gradient(circle at top, #1a1a1a, #000);
                color: white;
                font-family: 'Segoe UI', sans-serif;
                text-align: center;
            }
            h1 {
                font-size: 110px;
                letter-spacing: 12px;
                margin: 0;
                font-weight: 800;
                background: linear-gradient(90deg, #00ffe1, #00aaff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(0,255,225,.25);
            }
            p {
                opacity: .75;
            }
            a {
                color: #00ffe1;
                text-decoration: none;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <h1>HUNTER</h1>
        <p>Universal Media Downloader API</p>
        <p>Developer <a href="https://t.me/xoxhunterxd" target="_blank">@xoxhunterxd</a></p>
    </body>
    </html>
    """

# ================= DOWNLOAD API =================
@app.get("/api/download")
def download(url: str, request: Request):
    base_url = str(request.base_url).rstrip("/")

    try:
        data = download_media(url, base_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Browser → HTML
    if "text/html" in request.headers.get("accept", ""):
        return HTMLResponse(render_html_result(data))

    # API → JSON
    return JSONResponse(data)

# ================= FILE SERVING =================
@app.get("/api/download/file/{uid}/{filename}")
def get_file(uid: str, filename: str):
    path = os.path.join("downloads", uid, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path,
        filename=filename,
        media_type="application/octet-stream"
    )

# ================= HTML RESULT PAGE =================
def render_html_result(data: dict) -> str:
    buttons = ""

    for f in data["files"]:
        if f.endswith(".mp4"):
            label = "⬇ Download MP4"
        elif f.endswith(".mp3"):
            label = "⬇ Download MP3"
        elif f.endswith(".jpg") or f.endswith(".png"):
            label = "⬇ Download Image"
        else:
            label = "⬇ Download"

        buttons += f"""
        <button onclick="startDownload('{f}')">{label}</button>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data["title"]}</title>
        <style>
            body {{
                background: #0f0f0f;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
            }}
            .card {{
                background: #1a1a1a;
                padding: 40px;
                border-radius: 14px;
                text-align: center;
                width: 420px;
                box-shadow: 0 0 40px rgba(0,0,0,.6);
                z-index: 10;
            }}
            h2 {{
                margin-bottom: 8px;
            }}
            .platform {{
                opacity: .7;
                margin-bottom: 25px;
            }}
            button {{
                width: 100%;
                margin: 10px 0;
                padding: 14px;
                border-radius: 8px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
                background: linear-gradient(90deg, #00ffe1, #00aaff);
                color: #000;
            }}
            button:hover {{
                opacity: .85;
            }}
            .dev {{
                margin-top: 25px;
                font-size: 14px;
                opacity: .6;
            }}

            /* 🎉 CONFETTI */
            .confetti {{
                position: fixed;
                width: 8px;
                height: 8px;
                background: red;
                animation: fall 4s linear forwards;
            }}

            @keyframes fall {{
                0% {{ transform: translateY(-10px) rotate(0deg); }}
                100% {{ transform: translateY(110vh) rotate(720deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>{data["title"]}</h2>
            <div class="platform">{data["platform"]}</div>
            {buttons}
            <div class="dev">Developer {data["dev"]}</div>
        </div>

        <script>
            function startDownload(url) {{
                launchConfetti();

                // Start download
                const a = document.createElement("a");
                a.href = url;
                a.download = "";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }}

            function launchConfetti() {{
                for (let i = 0; i < 80; i++) {{
                    const confetti = document.createElement("div");
                    confetti.className = "confetti";
                    confetti.style.left = Math.random() * 100 + "vw";
                    confetti.style.background =
                        "hsl(" + Math.random() * 360 + ", 100%, 50%)";
                    confetti.style.animationDuration =
                        2 + Math.random() * 2 + "s";
                    document.body.appendChild(confetti);

                    setTimeout(() => confetti.remove(), 4000);
                }}
            }}
        </script>
    </body>
    </html>
    """
