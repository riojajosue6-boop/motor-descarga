import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
# Usamos el motor que indicaste que funcionaba bien
API_HOST = "download-all-in-one-lite.p.rapidapi.com" 

user_registry = {}

def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry[ip]['date'] != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

# --- INTERFAZ NEÓN PRO ---
HTML_INDEX = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀</title>
    <style>
        :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; }
        body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin:0; padding:15px; text-align:center; }
        .card { max-width: 450px; margin: auto; background: #121212; padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.1); }
        h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 8px var(--cian); margin-bottom: 5px; }
        .stats { display: flex; justify-content: space-around; font-size: 13px; margin: 20px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; }
        .stats b { color: var(--fucsia); font-size: 16px; }
        .input-group { position: relative; margin-bottom: 15px; }
        input { width: 100%; padding: 16px; border-radius: 12px; border: 1px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
        .btn-clear { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #222; color: #fff; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; }
        .btn-go { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; font-size: 18px; }
        #loader { display: none; margin-top: 20px; color: var(--cian); font-weight: bold; }
        #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
        .thumb { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 10px; }
        .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 20px; margin-top: 15px; font-weight: bold; }
        .dl-btn { background: #000; color: #fff; padding: 14px; text-decoration: none; border-radius: 12px; display: block; margin-top: 12px; font-size: 16px; }
        footer { margin-top: 40px; color: #444; font-size: 11px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>TurboLink</h1>
        <p style="font-size:10px; color:#555; margin-top:-5px;">PROPIEDAD DE TURBOLINK DIGITAL</p>
        
        <div class="stats">
            <div>YT/TikTok: <b id="p-count">-</b></div>
            <div>Social: <b id="s-count">-</b></div>
        </div>

        <div class="input-group">
            <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
            <button class="btn-clear" onclick="clearAll()">✕</button>
        </div>

        <button id="mainBtn" class="btn-go" onclick="start()">Generar Descarga</button>
        
        <div id="loader">🚀 Preparando video... <span id="clock">15</span>s</div>

        <div id="previewSection">
            <img id="vThumb" class="thumb" src="">
            <div id="vTitle" style="font-weight:bold; font-size:14px; margin-bottom:10px;"></div>
            <div class="dl-box">
                ✅ VIDEO LISTO
                <a id="vLink" href="" target="_blank" class="dl-btn">📥 GUARDAR AHORA</a>
            </div>
        </div>
        
        <div id="status" style="margin-top:15px; color:var(--fucsia); font-weight:bold;"></div>
    </div>
    <footer>© 2026 TurboLink Digital</footer>

    <script>
        async function getStats() {
            try {
                const r = await fetch('/api/user_info');
                const d = await r.json();
                document.getElementById('p-count').innerText = d.premium;
                document.getElementById('s-count').innerText = d.social;
            } catch(e){}
        }
        getStats();

        function clearAll() {
            document.getElementById('urlInput').value = '';
            document.getElementById('previewSection').style.display = 'none';
            document.getElementById('status').innerText = '';
            document.getElementById('mainBtn').disabled = false;
        }

        async function start() {
            const url = document.getElementById('urlInput').value;
            if(!url) return alert("Pega un link");
            
            const btn = document.getElementById('mainBtn');
            const loader = document.getElementById('loader');
            document.getElementById('previewSection').style.display = 'none';
            document.getElementById('status').innerText = '';

            btn.disabled = true;
            loader.style.display = "block";
            
            let t = 15;
            let i = setInterval(async () => {
                t--; document.getElementById('clock').innerText = t;
                if(t <= 0) {
                    clearInterval(i); loader.style.display = "none";
                    await fetchVideo(url);
                    btn.disabled = false;
                    getStats();
                }
            }, 1000);
        }

        async function fetchVideo(url) {
            const status = document.getElementById('status');
            const preview = document.getElementById('previewSection');
            status.innerText = "⏳ Extrayendo...";
            
            try {
                const r = await fetch('/api/get_info?url=' + encodeURIComponent(url));
                const d = await r.json();
                
                if(d.success) {
                    status.innerText = "";
                    document.getElementById('vThumb').src = d.thumbnail;
                    document.getElementById('vTitle').innerText = d.title;
                    document.getElementById('vLink').href = d.download_url;
                    preview.style.display = 'block';
                } else {
                    status.innerText = "❌ " + d.message;
                }
            } catch(e) { status.innerText = "❌ Error de servidor."; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

@app.route('/api/get_info')
def get_info():
    url = request.args.get('url')
    ip = request.remote_addr
    stats = check_user(ip)
    
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    if (is_p and stats['premium'] <= 0) or (not is_p and stats['social'] <= 0):
        return jsonify({"success": False, "message": "Cupos diarios agotados."})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.get(f"https://{API_HOST}/autolink", params={"url": url}, headers=headers, timeout=15)
        data = r.json()
        
        # Extraer link y miniatura de la API directamente
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        thumb = data.get('thumbnail')
        
        # Corrección de miniatura para YouTube si falla
        if not thumb and is_p:
            yid = get_yt_id(url)
            if yid: thumb = f"https://img.youtube.com/vi/{yid}/hqdefault.jpg"

        if dl_url:
            if is_p: stats['premium'] -= 1
            else: stats['social'] -= 1
            return jsonify({
                "success": True, 
                "download_url": dl_url, 
                "thumbnail": thumb or "", 
                "title": data.get("title", "Video Listo")
            })
    except: pass
    return jsonify({"success": False, "message": "Video no disponible o privado."})

if __name__ == "__main__":
    # Railway requiere el puerto de la variable de entorno
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)8080)))
