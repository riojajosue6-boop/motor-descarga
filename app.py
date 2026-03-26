import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
PROPIETARIO = "TurboLink Digital"
BLOG_SOPORTE = "https://tu-blog-aqui.blogspot.com"

# Registro de cuotas por IP
user_registry = {}

def get_clean_url(raw_url):
    match = re.search(r'(https?://[^\s]+)', raw_url)
    return match.group(1) if match else None

def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry[ip]['date'] != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

# --- INTERFAZ PREMIUM ---
HTML_MAIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀 | Descargas Pro</title>
    <style>
        :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; --card: #121212; }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; display: flex; justify-content: center; gap: 20px; }
        nav a { color: #888; text-decoration: none; cursor: pointer; font-size: 14px; }
        nav a:hover { color: var(--cian); }
        .container { padding: 20px; max-width: 480px; margin: 0 auto; }
        .main-card { background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.1); }
        h1 { color: var(--cian); font-size: 28px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 8px var(--cian); }
        .stats { display: flex; justify-content: space-around; font-size: 12px; margin: 15px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; }
        .stats b { color: var(--fucsia); font-size: 16px; }
        .input-group { position: relative; margin-bottom: 20px; }
        input { width: 100%; padding: 16px; border-radius: 12px; border: 1px solid #333; background: #000; color: #fff; box-sizing: border-box; outline: none; font-size: 16px; }
        .clear-btn { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #333; color: #fff; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; font-weight: bold; }
        #btnAction { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; transition: 0.3s; }
        #btnAction:hover { box-shadow: 0 0 15px var(--cian); }
        #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }
        #finalDownloadBtn { width: 100%; padding: 16px; background: #2ecc71; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 16px; }
        #finalDownloadBtn:disabled { background: #333; color: #777; cursor: not-allowed; }
        .support-box { background: rgba(46, 204, 113, 0.1); color: #2ecc71; padding: 15px; border-radius: 12px; font-size: 13px; margin: 15px 0; border: 1px dashed #2ecc71; }
        footer { margin-top: 40px; color: #444; font-size: 11px; }
        .legal-content { display: none; text-align: left; background: #111; padding: 20px; border-radius: 15px; margin-top: 20px; border: 1px solid #222; font-size: 14px; color: #aaa; }
    </style>
</head>
<body>
    <nav>
        <a onclick="show('home')">Inicio</a>
        <a onclick="show('privacy')">Privacidad</a>
        <a onclick="show('terms')">DMCA</a>
    </nav>

    <div class="container">
        <div id="home-sec">
            <div class="main-card">
                <h1>TurboLink 🚀</h1>
                <div class="stats">
                    <div>YT/TikTok: <b id="p-count">-</b></div>
                    <div>Redes: <b id="s-count">-</b></div>
                </div>
                <div class="input-group">
                    <input type="text" id="urlInput" placeholder="Pega el link aquí...">
                    <button class="clear-btn" onclick="clearUrl()">✕</button>
                </div>
                <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
                
                <div id="status" style="margin-top:15px; font-weight:bold; color: var(--cian);"></div>

                <div id="previewSection">
                    <img id="videoThumbnail" src="">
                    <div id="videoTitle" style="font-weight:bold; margin-bottom:10px;"></div>
                    <div class="support-box">
                        ❤️ <b>Apoyo:</b> Visita la publicidad para que el sitio siga gratis.<br>
                        <span id="countdownText" style="color:#fff;">Espera 15s...</span>
                    </div>
                    <a id="finalDownloadLink" style="text-decoration:none;">
                        <button id="finalDownloadBtn" disabled>DESCARGAR AHORA</button>
                    </a>
                </div>
            </div>
        </div>

        <div id="privacy-sec" class="legal-content">
            <h2>Privacidad</h2>
            <p>Usamos tu IP solo para limitar descargas diarias y proteger el servidor.</p>
        </div>

        <div id="terms-sec" class="legal-content">
            <h2>DMCA</h2>
            <p>TurboLink Digital no aloja archivos. Solo procesa links públicos mediante API.</p>
        </div>
    </div>

    <footer>© 2026 TurboLink Digital - Cochabamba 🇧🇴</footer>

    <script>
        async function getStats() {
            try {
                const r = await fetch('/api/user_info');
                const d = await r.json();
                document.getElementById('p-count').innerText = d.premium;
                document.getElementById('s-count').innerText = d.social;
            } catch(e) {}
        }
        getStats();

        function show(sec) {
            document.getElementById('home-sec').style.display = sec === 'home' ? 'block' : 'none';
            document.getElementById('privacy-sec').style.display = sec === 'privacy' ? 'block' : 'none';
            document.getElementById('terms-sec').style.display = sec === 'terms' ? 'block' : 'none';
        }

        function clearUrl() {
            document.getElementById('urlInput').value = "";
            document.getElementById('status').innerText = "";
            document.getElementById('previewSection').style.display = 'none';
            document.getElementById('btnAction').disabled = false;
        }

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            const dBtn = document.getElementById('finalDownloadBtn');
            
            if(!url) return alert("Pega un link");
            b.disabled = true;
            s.innerText = "⏳ Analizando...";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block'; 
                    s.innerText = "✅ Detectado";
                    
                    let timeLeft = 15;
                    dBtn.disabled = true;
                    const countdown = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `Activando en ${timeLeft}s...`;
                        if(timeLeft <= 0) {
                            clearInterval(countdown);
                            document.getElementById('countdownText').innerText = "¡Listo!";
                            dBtn.disabled = false;
                            getDownload(url);
                        }
                    }, 1000);
                } else { s.innerText = "❌ No disponible"; b.disabled = false; }
            } catch (e) { s.innerText = "❌ Error en servidor"; b.disabled = false; }
        }

        async function getDownload(url) {
            const res = await fetch('/api/down?url=' + encodeURIComponent(url));
            const data = await res.json();
            if(data.url) {
                document.getElementById('finalDownloadLink').href = data.url;
            } else {
                document.getElementById('status').innerText = "❌ Error al generar link";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_MAIN)

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

@app.route('/api/info')
def api_info():
    url = get_clean_url(request.args.get('url'))
    if not url: return jsonify({"success": False})
    
    ip = request.remote_addr
    stats = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and stats['premium'] <= 0) or (not is_p and stats['social'] <= 0):
        return jsonify({"success": False, "message": "Sin créditos"})

    try:
        # Usamos la API Lite para info rápida
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=10)
        data = r.json()
        thumb = data.get("thumbnail")
        if not thumb and ("youtube.com" in url or "youtu.be" in url):
            yid = get_yt_id(url)
            thumb = f"https://img.youtube.com/vi/{yid}/hqdefault.jpg"
        return jsonify({"success": True, "title": data.get("title", "Video"), "thumbnail": thumb})
    except: return jsonify({"success": False})

@app.route('/api/down')
def api_down():
    url = get_clean_url(request.args.get('url'))
    ip = request.remote_addr
    stats = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])

    try:
        headers = {"x-rapidapi-key": API_KEY}
        # YouTube usa motor específico
        if "youtube.com" in url or "youtu.be" in url:
            yid = get_yt_id(url)
            headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yid}, headers=headers, timeout=15)
            data = r.json()
            link = None
            for f in data.get('formats', []):
                if 'video' in f.get('mimeType', ''): link = f.get('url'); break
            final_url = link or data.get('link')
        else:
            # Redes sociales motor general
            headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=15)
            data = r.json()
            medias = data.get("medias", [])
            final_url = medias[0].get('url') if medias else None

        if final_url:
            if is_p: stats['premium'] -= 1
            else: stats['social'] -= 1
            return jsonify({"url": final_url})
    except: pass
    return jsonify({"error": "Error"}), 500

if __name__ == "__main__":
    # Cambiado a puerto 8080 que es el estándar de Railway para evitar el error 503
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
