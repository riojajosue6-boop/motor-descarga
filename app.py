import os
import requests
import re
import random
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD Y COSTOS ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_CONTACTO = "https://tu-blog-aqui.blogspot.com"

# LÍMITES DE SEGURIDAD (Plan 10GB)
MAX_MB_PLAN = 10000  # 10 GB de tope para no pagar excedentes
PESO_MAX_VIDEO = 15   # 15 MB por video (protege tus gigas)

# Base de datos en memoria (IPs y Consumo Global)
server_stats = {"total_mb": 0}
user_registry = {}

# Lista de "Disfraz" (User-Agents) para saltar bloqueos
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD2A.220121.002.A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36"
]

def get_clean_url(raw_url):
    match = re.search(r'(https?://[^\s]+)', raw_url)
    return match.group(1) if match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry[ip]['date'] != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

# --- INTERFAZ NEÓN (Fase 2) ---
@app.route('/')
def home():
    progreso = (server_stats["total_mb"] / MAX_MB_PLAN) * 100
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TurboLink 🚀 | Reels & Shorts</title>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; }
            body { background: var(--bg); color: white; font-family: sans-serif; margin:0; padding:15px; text-align:center; }
            .card { max-width: 450px; margin: auto; background: #121212; padding: 25px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 15px rgba(0,242,234,0.1); }
            h1 { color: var(--cian); text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 8px var(--cian); }
            .meter-box { background: #000; padding: 10px; border-radius: 12px; margin: 15px 0; border: 1px solid #222; }
            .progress-bar { height: 8px; background: #222; border-radius: 4px; overflow: hidden; }
            .progress-fill { height: 100%; background: var(--cian); width: {{p}}%; transition: 1s; }
            .stats { display: flex; justify-content: space-around; font-size: 13px; margin: 15px 0; color: #aaa; }
            .stats b { color: var(--fucsia); }
            input { width: 100%; padding: 15px; border-radius: 12px; border: 2px solid #222; background: #000; color: #fff; box-sizing: border-box; margin-bottom: 10px; }
            .btn-go { width: 100%; padding: 16px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            .footer { margin-top: 30px; font-size: 11px; color: #444; line-height: 1.8; }
            .footer a { color: var(--cian); text-decoration: none; }
            #timer { display: none; margin-top: 15px; color: var(--cian); font-weight: bold; border: 1px dashed #333; padding: 10px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TurboLink</h1>
            <div class="meter-box">
                <div class="progress-bar"><div class="progress-fill"></div></div>
                <p style="font-size:10px; color:#555; margin: 5px 0 0;">GASOLINA DEL SERVIDOR: {{c}}/{{m}} MB</p>
            </div>
            <div class="stats">
                <div>YT/TikTok: <b id="p-count">-</b></div>
                <div>FB/IG/Reels: <b id="s-count">-</b></div>
            </div>
            <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            <button id="btn" class="btn-go" onclick="start()">Generar Video</button>
            <div id="timer">🚀 Sincronizando con servidor seguro... <span id="clock">15</span>s</div>
            <div id="status" style="margin-top:20px;"></div>
        </div>
        <div class="footer">
            <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a> | <a href="{{blog}}" target="_blank">Soporte Blog</a><br>
            © 2026 TurboLink Digital.
        </div>
        <script>
            async function getStats() {
                const r = await fetch('/api/user_info'); const d = await r.json();
                document.getElementById('p-count').innerText = d.premium;
                document.getElementById('s-count').innerText = d.social;
            }
            getStats();
            async function start() {
                const url = document.getElementById('urlInput').value; if(!url) return;
                const btn = document.getElementById('btn'); const clockBox = document.getElementById('timer');
                btn.disabled = true; clockBox.style.display = "block";
                let t = 15;
                let i = setInterval(async () => {
                    t--; document.getElementById('clock').innerText = t;
                    if(t <= 0) {
                        clearInterval(i); clockBox.style.display = "none";
                        await process(url); btn.disabled = false; getStats();
                    }
                }, 1000);
            }
            async function process(url) {
                const status = document.getElementById('status'); status.innerHTML = "⏳ Extrayendo...";
                try {
                    const r = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        status.innerHTML = `<div style="background:#2ecc71; color:000; padding:15px; border-radius:15px;">✅ LISTO<br><a href="/api/download?v=${encodeURIComponent(d.url)}" style="background:#000; color:#fff; display:block; padding:10px; margin-top:10px; border-radius:8px; text-decoration:none; font-weight:bold;">📥 GUARDAR MP4</a></div>`;
                    } else { status.innerHTML = "<b style='color:red;'>" + d.message + "</b>"; }
                } catch(e) { status.innerHTML = "❌ Error técnico."; }
            }
        </script>
    </body>
    </html>
    ''', p=progreso, c=int(server_stats["total_mb"]), m=MAX_MB_PLAN, blog=BLOG_CONTACTO)

# --- LÓGICA DE API Y TÚNEL (Fase 3) ---

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

@app.route('/api/fetch')
def fetch_api():
    if server_stats["total_mb"] >= MAX_MB_PLAN:
        return jsonify({"success": False, "message": "Servidor lleno. Vuelve mañana."})
    
    raw_url = request.args.get('url')
    clean_url = get_clean_url(raw_url)
    if not clean_url: return jsonify({"success": False, "message": "Link no detectado."})

    ip = request.remote_addr
    st = check_user(ip)
    is_p = any(x in clean_url for x in ["tiktok", "youtube", "youtu.be"])

    if (is_p and st['premium'] <= 0) or (not is_p and st['social'] <= 0):
        return jsonify({"success": False, "message": "Sin créditos para hoy."})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=12)
        v_url = r.json().get('url')
        if v_url:
            if is_p: st['premium'] -= 1
            else: st['social'] -= 1
            return jsonify({"success": True, "url": v_url})
    except: pass
    return jsonify({"success": False, "message": "Video no disponible o privado."})

@app.route('/api/download')
def proxy_tunnel():
    v_url = request.args.get('v')
    # CAPA DE CAMUFLAJE: Disfrazamos la petición
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': '*/*',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        req = requests.get(v_url, headers=headers, stream=True, timeout=25)
        
        def stream_video():
            for chunk in req.iter_content(chunk_size=1024*512): # 0.5MB chunks
                if chunk:
                    server_stats["total_mb"] += 0.5 # Sumar al contador global
                    if server_stats["total_mb"] > MAX_MB_PLAN: break # Freno de emergencia
                    yield chunk

        res = Response(stream_with_context(stream_video()), content_type='video/mp4')
        res.headers['Content-Disposition'] = 'attachment; filename="TurboLink_Video.mp4"'
        return res
    except:
        return "Error en la conexión segura", 500

# --- LEGALES ---
@app.route('/privacidad')
def privacy():
    return f"<h1>Privacidad - {PROPIETARIO}</h1><p>Usamos tu IP solo para el límite de 5 descargas diarias.</p>"

@app.route('/dmca')
def dmca_page():
    return f"<h1>DMCA - {PROPIETARIO}</h1><p>TurboLink no aloja videos. Es un puente técnico para archivos públicos.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
