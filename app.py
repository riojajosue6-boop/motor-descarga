import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_SOPORTE = "https://tu-blog-aquí.blogspot.com"

user_registry = {}

def get_clean_url(raw_url):
    match = re.search(r'(https?://[^\s]+)', raw_url)
    return match.group(1) if match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry[ip]['date'] != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TurboLink 🚀 | Descargas Reales</title>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; }
            body { background: var(--bg); color: white; font-family: sans-serif; margin:0; padding:15px; text-align:center; }
            .card { max-width: 450px; margin: auto; background: #121212; padding: 25px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.15); }
            h1 { color: var(--cian); text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 8px var(--cian); }
            .stats { display: flex; justify-content: space-around; font-size: 13px; margin: 20px 0; background: #1a1a1a; padding: 15px; border-radius: 12px; }
            .stats b { color: var(--fucsia); font-size: 16px; }
            .input-wrapper { position: relative; width: 100%; margin-bottom: 15px; }
            input { width: 100%; padding: 15px 45px 15px 15px; border-radius: 12px; border: 2px solid #222; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; }
            .btn-clear { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: #222; color: #888; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; }
            .btn-go { width: 100%; padding: 16px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            #loader { display: none; margin-top: 15px; color: var(--cian); font-weight: bold; }
            .thumb { width: 100%; border-radius: 15px; margin-top: 15px; border: 2px solid #333; display: none; }
            .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 20px; margin-top: 20px; font-weight: bold; }
            .dl-btn { background: #000; color: #fff; padding: 14px; text-decoration: none; border-radius: 12px; display: block; margin-top: 10px; font-size: 16px; }
            .footer { margin-top: 40px; font-size: 11px; color: #444; }
            .footer a { color: var(--cian); text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TurboLink</h1>
            <div class="stats">
                <div>YT/TikTok: <b id="p-count">-</b></div>
                <div>Social: <b id="s-count">-</b></div>
            </div>
            <div class="input-wrapper">
                <input type="text" id="urlInput" placeholder="Pega el link aquí...">
                <button class="btn-clear" onclick="clearAll()">×</button>
            </div>
            <button id="btn" class="btn-go" onclick="start()">GENERAR VIDEO</button>
            <div id="loader">🚀 Preparando archivo... <span id="clock">15</span>s</div>
            <img id="preview" class="thumb">
            <div id="status"></div>
        </div>
        <div class="footer">
            <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a> | <a href="{{blog}}" target="_blank">Soporte</a>
            <p>© 2026 TurboLink Digital.</p>
        </div>
        <script>
            async function getStats() {
                const r = await fetch('/api/user_info'); const d = await r.json();
                document.getElementById('p-count').innerText = d.premium;
                document.getElementById('s-count').innerText = d.social;
            }
            getStats();
            function clearAll() {
                document.getElementById('urlInput').value = '';
                document.getElementById('status').innerHTML = '';
                document.getElementById('preview').style.display = 'none';
                document.getElementById('loader').style.display = 'none';
                document.getElementById('btn').disabled = false;
                getStats();
            }
            async function start() {
                const url = document.getElementById('urlInput').value; if(!url) return;
                const btn = document.getElementById('btn'); const loader = document.getElementById('loader');
                document.getElementById('status').innerHTML = ''; document.getElementById('preview').style.display = 'none';
                btn.disabled = true; loader.style.display = "block";
                let t = 15;
                let i = setInterval(async () => {
                    t--; document.getElementById('clock').innerText = t;
                    if(t <= 0) { clearInterval(i); loader.style.display = "none"; await process(url); btn.disabled = false; getStats(); }
                }, 1000);
            }
            async function process(url) {
                const status = document.getElementById('status'); const preview = document.getElementById('preview');
                status.innerHTML = "⏳ Extrayendo...";
                try {
                    const r = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        if(d.thumbnail) { preview.src = d.thumbnail; preview.style.display = 'block'; }
                        status.innerHTML = `<div class="dl-box">✅ ¡LISTO!<a href="/api/download?v=${encodeURIComponent(d.url)}" class="dl-btn">📥 DESCARGAR AHORA</a></div>`;
                    } else { status.innerHTML = "<b style='color:red;'>" + d.message + "</b>"; }
                } catch(e) { status.innerHTML = "❌ Error de conexión."; }
            }
        </script>
    </body>
    </html>
    ''', blog=BLOG_SOPORTE)

@app.route('/api/user_info')
def user_info(): return jsonify(check_user(request.remote_addr))

@app.route('/api/fetch')
def fetch_api():
    raw_url = request.args.get('url')
    clean_url = get_clean_url(raw_url)
    if not clean_url: return jsonify({"success": False, "message": "Link no detectado."})
    ip = request.remote_addr
    st = check_user(ip)
    is_p = any(x in clean_url for x in ["tiktok", "youtube", "youtu.be"])
    if (is_p and st['premium'] <= 0) or (not is_p and st['social'] <= 0):
        return jsonify({"success": False, "message": "Sin créditos hoy."})
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=12)
        res = r.json()
        video_url = res.get('url')
        thumb = res.get('thumbnail') or res.get('picture')
        if video_url:
            if is_p: st['premium'] -= 1
            else: st['social'] -= 1
            return jsonify({"success": True, "url": video_url, "thumbnail": thumb})
    except: pass
    return jsonify({"success": False, "message": "Video no disponible."})

@app.route('/api/download')
def force_download():
    # ESTE ES EL SECRETO: El servidor descarga el video y se lo pasa al celular como un archivo
    video_url = request.args.get('v')
    r = requests.get(video_url, stream=True, timeout=25)
    
    def generate():
        total = 0
        for chunk in r.iter_content(chunk_size=1024*1024):
            total += len(chunk)
            if total > 15*1024*1024: break # Límite de 15MB para cuidar tu plan
            yield chunk

    # Forzamos que el navegador lo vea como una descarga de video MP4
    return Response(stream_with_context(generate()), 
                    content_type='video/mp4',
                    headers={'Content-Disposition': 'attachment; filename="TurboLink_Video.mp4"'})

@app.route('/privacidad')
def privacy(): return "<h1>Privacidad</h1>"

@app.route('/dmca')
def dmca_page(): return "<h1>DMCA</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
