import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- DATOS DE LA API (NETO) ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "download-all-in-one-lite.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_SOPORTE = "https://tu-blog-aqui.blogspot.com"

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
        <title>TurboLink 🚀</title>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; }
            body { background: var(--bg); color: white; font-family: sans-serif; margin:0; padding:15px; text-align:center; }
            .card { max-width: 450px; margin: auto; background: #121212; padding: 25px; border-radius: 25px; border: 1px solid #333; }
            h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 8px var(--cian); }
            .stats { display: flex; justify-content: space-around; font-size: 12px; margin: 20px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; }
            .stats b { color: var(--fucsia); font-size: 16px; }
            input { width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; margin-bottom: 10px; }
            .btn-go { width: 100%; padding: 16px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }
            .thumb { width: 100%; border-radius: 15px; margin-top: 15px; border: 1px solid #333; display: none; }
            .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 20px; margin-top: 20px; font-weight: bold; }
            .dl-btn { background: #000; color: #fff; padding: 14px; text-decoration: none; border-radius: 12px; display: block; margin-top: 10px; }
            #loader { display: none; margin-top: 15px; color: var(--cian); font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TurboLink</h1>
            <div class="stats">
                <div>YT/TikTok: <b id="p-count">-</b></div>
                <div>Redes: <b id="s-count">-</b></div>
            </div>
            <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            <button id="btn" class="btn-go" onclick="start()">PROCESAR</button>
            <div id="loader">🚀 Preparando... <span id="clock">15</span>s</div>
            <img id="preview" class="thumb">
            <div id="status"></div>
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
                        status.innerHTML = `<div class="dl-box">✅ ¡LISTO!<a href="${d.url}" target="_blank" class="dl-btn">📥 DESCARGAR VIDEO</a></div>`;
                    } else { status.innerHTML = "<b style='color:red;'>" + d.message + "</b>"; }
                } catch(e) { status.innerHTML = "❌ Error de conexión."; }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/user_info')
def user_info(): return jsonify(check_user(request.remote_addr))

@app.route('/api/fetch')
def fetch_api():
    url = get_clean_url(request.args.get('url'))
    if not url: return jsonify({"success": False, "message": "Link inválido."})
    ip = request.remote_addr
    st = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and st['premium'] <= 0) or (not is_p and st['social'] <= 0):
        return jsonify({"success": False, "message": "Cupo agotado."})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.get(f"https://{API_HOST}/autolink", params={"url": url}, headers=headers, timeout=12)
        data = r.json()
        video_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        thumb = data.get('thumbnail')
        
        if video_url:
            if is_p: st['premium'] -= 1
            else: st['social'] -= 1
            return jsonify({"success": True, "url": video_url, "thumbnail": thumb})
    except: pass
    return jsonify({"success": False, "message": "Video no disponible."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
