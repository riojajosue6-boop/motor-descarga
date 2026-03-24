import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES USA ---
def get_ydl_opts():
    user = "ksvyuzxs-us-rotate" 
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'socket_timeout': 30
    }

# --- INTERFAZ PREMIUM ---
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 30px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: 40px auto; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 28px; }
        .input-group { position: relative; margin: 25px 0; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; box-sizing: border-box; outline: none; }
        .btn-clear { position: absolute; right: 10px; top: 18px; background: #444; border: none; color: #fff; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; }
        #mainBtn { width: 100%; padding: 18px; background: #fff; color: #000; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        #mainBtn:disabled { opacity: 0.5; cursor: not-allowed; }
        .progress-container { margin: 20px 0; background: #222; border-radius: 10px; height: 10px; display: none; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: var(--primary); transition: 1s linear; }
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 18px; border-radius: 12px; text-decoration: none; font-weight: bold; margin-top: 20px; animation: glow 1.5s infinite alternate; }
        @keyframes glow { from { box-shadow: 0 0 5px var(--success); } to { box-shadow: 0 0 20px var(--success); transform: scale(1.02); } }
        .footer { margin-top: 50px; font-size: 11px; color: #444; }
        .footer a { color: #666; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p style="color:#666; font-size:11px; letter-spacing:1px; margin-top:5px;">TIKTOK • INSTAGRAM • FACEBOOK</p>
        <div class="input-group">
            <input type="text" id="urlInput" placeholder="Pega el link aquí..." autocomplete="off">
            <button class="btn-clear" onclick="document.getElementById('urlInput').value=''">✕</button>
        </div>
        <button id="mainBtn" onclick="procesar()">DESCARGAR VIDEO</button>
        <div id="result">
            <p id="status" style="color:#888; font-size:14px; margin-top:20px;"></p>
            <div class="progress-container" id="pContainer"><div class="progress-bar" id="pBar"></div></div>
            <a id="dlLink" class="dl-btn" href="#">DESCARGAR AHORA</a>
        </div>
    </div>
    <div class="footer">
        <a href="/privacidad">Privacidad</a> • <a href="/terminos">Términos</a>
        <p>© 2026 Motor Pro - Cochabamba 🇧🇴</p>
    </div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const btn = document.getElementById('mainBtn');
            const pBar = document.getElementById('pBar');
            const pContainer = document.getElementById('pContainer');
            const dlLink = document.getElementById('dlLink');
            if(!url) return;
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerText = "⏳ Extrayendo video (Proxy USA)...";
            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = "✅ ¡Video listo!<br><small>Preparando descarga segura en 8s...</small>";
                    pContainer.style.display = 'block';
                    let seg = 8;
                    const timer = setInterval(() => {
                        seg--;
                        pBar.style.width = ((8-seg)/8)*100 + "%";
                        if(seg <= 0) {
                            clearInterval(timer);
                            pContainer.style.display = 'none';
                            status.innerHTML = "<span style='color:lime'>¡ENLACE ACTIVADO!</span>";
                            dlLink.href = "/descargar_archivo?url=" + encodeURIComponent(data.url);
                            dlLink.style.display = 'block';
                            btn.disabled = false;
                        }
                    }, 1000);
                } else {
                    status.innerText = "❌ No se pudo obtener el video.";
                    btn.disabled = false;
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión.";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home(): 
    return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    if "?" in u: u = u.split("?")[0]
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url')})
    except: 
        return jsonify({"success": False})

@app.route('/descargar_archivo')
def descargar_archivo():
    video_url = request.args.get('url')
    if not video_url: return "Error"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': '
