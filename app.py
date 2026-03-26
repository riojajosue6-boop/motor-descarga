import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"

# Registro de cuotas por IP (2 para YT/TK, 3 para el resto)
user_registry = {}

def get_clean_url(raw_url):
    match = re.search(r'(https?://[^\s]+)', raw_url)
    return match.group(1) if match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry.get(ip, {}).get('date') != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

# --- INTERFAZ PRINCIPAL ---
HTML_MAIN = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀 | Descargas Pro</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
    <style>
        :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; --card: #121212; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { max-width: 450px; margin: 20px auto; background: var(--card); padding: 25px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.15); }
        h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 10px var(--cian); margin-bottom: 5px; }
        .stats { display: flex; justify-content: space-around; font-size: 12px; margin: 15px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; border: 1px solid #222; }
        .stats b { color: var(--fucsia); font-size: 16px; }
        .input-group { position: relative; margin-bottom: 20px; }
        input { width: 100%; padding: 16px; border-radius: 12px; border: 2px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
        .btn-clear { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #222; color: #fff; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; font-weight: bold; }
        .btn-main { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
        #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
        .thumb { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 15px; }
        .support-msg { background: rgba(0, 242, 234, 0.05); color: #2ecc71; padding: 15px; border-radius: 15px; font-size: 13px; line-height: 1.5; border: 1px dashed #00f2ea; text-align: left; }
        .btn-dl { width: 100%; padding: 18px; background: #2ecc71; color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 17px; cursor: pointer; margin-top: 15px; text-decoration: none; display: block; }
        .btn-dl:disabled { background: #333; color: #777; cursor: not-allowed; }
        footer { margin-top: 40px; font-size: 11px; color: #444; }
        footer a { color: var(--cian); text-decoration: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>TurboLink</h1>
        <div class="stats">
            <div>YT/TikTok: <b id="p-count">-</b></div>
            <div>Social: <b id="s-count">-</b></div>
        </div>
        <div class="input-group">
            <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
            <button class="btn-clear" onclick="resetAll()">✕</button>
        </div>
        <button id="btnAction" class="btn-main" onclick="analyze()">GENERAR DESCARGA</button>
        <div id="status" style="margin-top:15px; font-weight:bold; color: var(--cian);"></div>

        <div id="previewSection">
            <img id="vThumb" class="thumb" src="">
            <div class="support-msg">
                🚀 <b>¡Video Detectado!</b><br>
                Estamos preparando tu descarga. <b>Te invitamos a visitar nuestros anuncios</b>; esto nos ayuda a mantener este servicio gratuito para toda Bolivia. ¡Gracias!
                <br><br>
                <span id="timerText" style="color:#fff; font-size:18px; font-weight:bold;">Preparando en 12s...</span>
            </div>
            <a id="finalLink" href="" class="btn-dl" style="display:none;" target="_blank">DESCARGAR VIDEO</a>
            <button id="waitBtn" class="btn-dl" disabled>DESCARGAR VIDEO</button>
        </div>
    </div>
    <footer>
        <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a>
        <p>© 2026 TurboLink Digital</p>
    </footer>

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

        function resetAll() {
            document.getElementById('urlInput').value = '';
            document.getElementById('previewSection').style.display = 'none';
            document.getElementById('status').innerText = '';
            document.getElementById('btnAction').disabled = false;
        }

        async function analyze() {
            const url = document.getElementById('urlInput').value; if(!url) return;
            const btn = document.getElementById('btnAction');
            const status = document.getElementById('status');
            const preview = document.getElementById('previewSection');
            
            btn.disabled = true; status.innerText = "⏳ Analizando...";
            
            try {
                const r = await fetch('/api/get_info?url=' + encodeURIComponent(url));
                const d = await r.json();
                if(d.success) {
                    status.innerText = "✅ Video Encontrado";
                    document.getElementById('vThumb').src = d.thumbnail;
                    // Abrimos el reproductor nativo del navegador
                    document.getElementById('finalLink').href = "/player?v=" + encodeURIComponent(d.download_url);
                    preview.style.display = 'block';

                    let timeLeft = 12;
                    const timerText = document.getElementById('timerText');
                    const waitBtn = document.getElementById('waitBtn');
                    const finalLink = document.getElementById('finalLink');
                    
                    const timer = setInterval(() => {
                        timeLeft--;
                        timerText.innerText = `Preparando en ${timeLeft}s...`;
                        if(timeLeft <= 0) {
                            clearInterval(timer);
                            timerText.innerText = "¡Listo!";
                            waitBtn.style.display = 'none';
                            finalLink.style.display = 'block';
                            getStats();
                        }
                    }, 1000);
                } else { status.innerText = "❌ No disponible."; btn.disabled = false; }
            } catch(e) { status.innerText = "❌ Error técnico."; btn.disabled = false; }
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
    ip = request.remote_addr
    return jsonify(check_user(ip))

@app.route('/api/get_info')
def get_info():
    url = get_clean_url(request.args.get('url'))
    ip = request.remote_addr
    stats = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and stats['premium'] <= 0) or (not is_p and stats['social'] <= 0):
        return jsonify({"success": False, "message": "Cupos agotados hoy."})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST, "Content-Type": "application/json"}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        data = r.json()
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        if dl_url:
            if is_p: stats['premium'] -= 1
            else: stats['social'] -= 1
            return jsonify({
                "success": True, 
                "download_url": dl_url, 
                "thumbnail": data.get('thumbnail') or data.get('picture') or "",
                "title": data.get("title", "Video TurboLink")
            })
    except: pass
    return jsonify({"success": False})

@app.route('/player')
def player():
    # Esta página imita el comportamiento de googlevideo.com que viste en tu foto
    video_url = request.args.get('v')
    return render_template_string('''
    <html>
    <head><title>TurboLink Player</title></head>
    <body style="margin:0; background:#000; display:flex; align-items:center; justify-content:center;">
        <video controls autoplay style="max-width:100%; max-height:100%;">
            <source src="/stream?v={{v}}" type="video/mp4">
        </video>
    </body>
    </html>
    ''', v=video_url)

@app.route('/stream')
def stream():
    # Engañamos a Facebook enviando el video desde Railway como un flujo puro
    video_url = request.args.get('v')
    r = requests.get(video_url, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
    return Response(stream_with_context(r.iter_content(chunk_size=1024*1024)), content_type='video/mp4')

@app.route('/privacidad')
def privacy(): return "<h1>Privacidad</h1>"

@app.route('/dmca')
def dmca(): return "<h1>DMCA</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
