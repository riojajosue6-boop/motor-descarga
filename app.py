import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_CONTACTO = "https://tu-blog-aqui.blogspot.com" 

user_data = {}

def get_user_stats(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_data or user_data[ip].get('date') != today:
        user_data[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_data[ip]

# --- INTERFAZ NEÓN ---
HTML_MAIN = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀</title>
    <style>
        :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; --card: #121212; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; padding:15px; text-align:center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 25px; border-radius: 20px; border: 1px solid #333; }
        h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 10px var(--cian); }
        .stats { display: flex; justify-content: space-around; background: #1a1a1a; padding: 12px; border-radius: 12px; margin: 20px 0; font-size: 13px; }
        .stat-item b { color: var(--fucsia); }
        input { width: 100%; padding: 15px; border-radius: 12px; border: 2px solid #222; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; }
        .btn-motor { width: 100%; padding: 16px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; margin-top:10px; }
        .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 15px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 12px; text-decoration: none; border-radius: 8px; display: block; margin-top: 10px; font-weight: bold; }
        .footer { margin-top: 40px; font-size: 11px; color: #444; }
        .footer a { color: var(--cian); text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TurboLink</h1>
        <div class="stats">
            <div>YT/TikTok: <b id="p-count">-</b></div>
            <div>Redes: <b id="s-count">-</b></div>
        </div>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" class="btn-motor" onclick="startProcess()">GENERAR DESCARGA</button>
        <div id="timer-box" style="display:none; margin-top:15px;">⏳ Calentando motor... <b id="clock">15</b>s</div>
        <div id="status"></div>
    </div>
    <div class="footer">
        <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a> | <a href="{{ blog_url }}" target="_blank">Reclamos</a><br>
        © 2026 TurboLink Digital.
    </div>
    <script>
        async function updateStats() {
            const r = await fetch('/api/stats'); const d = await r.json();
            document.getElementById('p-count').innerText = d.premium;
            document.getElementById('s-count').innerText = d.social;
        }
        updateStats();
        async function startProcess() {
            const url = document.getElementById('urlInput').value; if(!url) return;
            const btn = document.getElementById('mainBtn'); const tBox = document.getElementById('timer-box');
            btn.disabled = true; tBox.style.display = "block";
            let time = 15;
            let inv = setInterval(async () => {
                time--; document.getElementById('clock').innerText = time;
                if(time <= 0) { clearInterval(inv); tBox.style.display = "none"; await fetchVideo(url); btn.disabled = false; updateStats(); }
            }, 1000);
        }
        async function fetchVideo(url) {
            const status = document.getElementById('status'); status.innerHTML = "⏳ Extrayendo...";
            try {
                const r = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const d = await r.json();
                if(d.success) {
                    status.innerHTML = `<div class="dl-box">✅ ¡LISTO!<a href="/api/download?v=${encodeURIComponent(d.url)}" class="dl-btn">📥 GUARDAR VIDEO</a><small>Protección de 1GB activa (Máx 15MB)</small></div>`;
                } else { status.innerHTML = "❌ " + d.message; }
            } catch(e) { status.innerHTML = "❌ Error."; }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_MAIN, blog_url=BLOG_CONTACTO)

@app.route('/api/stats')
def stats(): return jsonify(get_user_stats(request.remote_addr))

@app.route('/api/fetch')
def fetch_api():
    url = request.args.get('url')
    ip = request.remote_addr
    st = get_user_stats(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and st['premium'] <= 0) or (not is_p and st['social'] <= 0):
        return jsonify({"success": False, "message": "Cupo agotado"})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        v_url = r.json().get('url')
        if v_url:
            if is_p: st['premium'] -= 1
            else: st['social'] -= 1
            return jsonify({"success": True, "url": v_url})
    except: pass
    return jsonify({"success": False, "message": "Error al extraer"})

@app.route('/api/download')
def tunnel():
    v_url = request.args.get('v')
    # ESTO DISFRAZA A RAILWAY COMO UN NAVEGADOR REAL PARA QUE NO BAJE .HTML
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36'}
    try:
        r = requests.get(v_url, headers=headers, stream=True, timeout=20)
        def generate():
            total = 0
            for chunk in r.iter_content(chunk_size=1024*512): # Chunks de 512KB
                total += len(chunk)
                if total > 15*1024*1024: break # CORTE DE SEGURIDAD A LOS 15MB
                yield chunk
        return Response(stream_with_context(generate()), content_type='video/mp4', headers={'Content-Disposition': 'attachment; filename="TurboLink_Video.mp4"'})
    except: return "Error en descarga", 500

@app.route('/privacidad')
def privacy(): return f"<h1>Privacidad - {PROPIETARIO}</h1><p>Usamos tu IP para limitar las 5 descargas diarias.</p>"

@app.route('/dmca')
def dmca(): return f"<h1>DMCA - {PROPIETARIO}</h1><p>TurboLink no aloja videos, actúa como puente técnico.</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
