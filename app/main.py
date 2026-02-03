@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HUNTER</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">

<style>
* { box-sizing: border-box; }

body {
  margin: 0;
  background: radial-gradient(circle at top, #111 0%, #000 70%);
  font-family: Arial, sans-serif;
  color: white;
  overflow: hidden;
}

/* LOADER */
#loader {
  position: fixed;
  inset: 0;
  background: black;
  z-index: 100;
  display: flex;
  align-items: center;
}
#progress {
  height: 3px;
  width: 0%;
  background: linear-gradient(90deg,#00ffe1,#7f00ff,#ff0080);
  transition: width .2s;
}

/* INTRO */
#intro {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: black;
  z-index: 90;
}
#introText {
  font-family: 'Great Vibes', cursive;
  font-size: 44px;
  white-space: nowrap;
  overflow: hidden;
  border-right: 2px solid white;
  animation: typing 4s steps(50), blink .7s infinite;
}
@keyframes typing { from{width:0} to{width:100%} }
@keyframes blink { 50%{border-color:transparent} }

/* CANVAS */
canvas {
  position: fixed;
  inset: 0;
  z-index: 1;
}

/* MAIN */
#main {
  opacity: 0;
  transition: opacity 2s ease;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 2;
}

.container {
  text-align: center;
  padding: 40px;
}

/* NEON LOGO */
.logo {
  font-size: 90px;
  font-weight: 900;
  letter-spacing: 10px;
  background: linear-gradient(270deg,#00ffe1,#7f00ff,#ff0080,#00ffe1);
  background-size: 600% 600%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradient 6s ease infinite;
  text-shadow: 0 0 40px rgba(0,255,225,.3);
}
@keyframes gradient {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

/* SUBTITLE */
#typingSubtitle {
  margin-top: 20px;
  font-size: 20px;
  opacity: .85;
  height: 24px;
}

/* ICONS */
.icons {
  margin-top: 30px;
  font-size: 36px;
}
.icons span { margin: 0 15px; }

/* BUTTONS */
.buttons { margin-top: 40px; }
.btn {
  display: inline-block;
  margin: 10px;
  padding: 14px 30px;
  border-radius: 30px;
  background: linear-gradient(135deg,#00ffe1,#7f00ff);
  color: black;
  text-decoration: none;
  font-weight: bold;
  box-shadow: 0 0 25px rgba(0,255,225,.5);
}

/* FOOTER */
.footer {
  margin-top: 40px;
  font-size: 14px;
  opacity: .6;
}

/* MOUSE GLOW */
#glow {
  position: fixed;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle,#00ffe1 0%,transparent 70%);
  pointer-events: none;
  opacity: .15;
  mix-blend-mode: screen;
  z-index: 0;
}
</style>
</head>

<body>

<div id="loader"><div id="progress"></div></div>

<div id="intro">
  <div id="introText">THIS SITE IS MADE BY SANDEEP (@xoxhunterxd)</div>
</div>

<canvas id="particles"></canvas>
<canvas id="fireworks"></canvas>
<div id="glow"></div>

<div id="main">
  <div class="container">
    <div class="logo">HUNTER</div>
    <div id="typingSubtitle"></div>

    <div class="icons">
      ▶️ 📸 🎵
    </div>

    <div class="buttons">
      <a class="btn" href="https://t.me/xoxhunterxd" target="_blank">Telegram</a>
      <a class="btn" href="mailto:topxoxhunter@gmail.com">Email</a>
      <a class="btn" href="/docs">API Docs</a>
    </div>

    <div class="footer">
      Developer @xoxhunterxd • MP4 • MP3 • Images
    </div>
  </div>
</div>

<script>
/* LOADER */
let p = 0;
const prog = document.getElementById("progress");
const loadInt = setInterval(()=>{
  p += Math.random()*10;
  prog.style.width = Math.min(p,100)+"%";
  if(p>=100){
    clearInterval(loadInt);
    document.getElementById("loader").style.display="none";
  }
},200);

/* INTRO → FIREWORKS → MAIN */
setTimeout(()=>{
  fireworksExplosion();
},4500);

setTimeout(()=>{
  document.getElementById("intro").style.display="none";
  document.getElementById("main").style.opacity=1;
},5500);

/* TYPING */
const text="Universal Media Downloader API";
let i=0;
setInterval(()=>{
  if(i<text.length)
    document.getElementById("typingSubtitle").textContent+=text[i++];
},80);

/* PARTICLES */
const c=document.getElementById("particles"),ctx=c.getContext("2d");
c.width=innerWidth;c.height=innerHeight;
let parts=[...Array(120)].map(()=>({
  x:Math.random()*c.width,y:Math.random()*c.height,
  r:Math.random()*2+1,dx:(Math.random()-.5),dy:(Math.random()-.5)
}));
function animate(){
  ctx.clearRect(0,0,c.width,c.height);
  ctx.fillStyle="#00ffe1";
  parts.forEach(p=>{
    p.x+=p.dx;p.y+=p.dy;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();
  });
  requestAnimationFrame(animate);
}
animate();

/* FIREWORKS */
const fw=document.getElementById("fireworks"),fctx=fw.getContext("2d");
fw.width=innerWidth;fw.height=innerHeight;
function fireworksExplosion(){
  for(let i=0;i<80;i++){
    let x=fw.width/2,y=fw.height/2;
    let vx=(Math.random()-.5)*6,vy=(Math.random()-.5)*6;
    let life=60;
    (function draw(){
      if(life--<=0)return;
      fctx.fillStyle="rgba(255,255,255,.8)";
      fctx.fillRect(x,y,3,3);
      x+=vx;y+=vy;
      requestAnimationFrame(draw);
    })();
  }
}

/* MOUSE GLOW */
const glow=document.getElementById("glow");
document.addEventListener("mousemove",e=>{
  glow.style.left=e.clientX-100+"px";
  glow.style.top=e.clientY-100+"px";
});
</script>

</body>
</html>
    """
