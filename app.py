import os
import requests
import re
import base64
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime
import urllib.parse

app = Flask(__name__)

# --- CONFIGURACIÓN MAESTRA TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
# Usamos tu API Pro comprada
API_HOST = "auto-download-all-in-one.p.rapidapi.com"

user_registry = {}

def get_clean_url(raw_url):
    # Extrae solo la URL real, ignorando basura técnica de la consola
    url_match = re.search(r'(https?://[^\s\'"<>]+)', raw_url)
    return url_match.group(1) if url_match else None

def check_user(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_registry or user_registry.get(ip, {}).get('date') != today:
        user_registry[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_registry[ip]

@app.route('/')
def home():
    return render_template_string('''
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
            .stats { display: flex; justify-content: space-around; font-size: 12px; margin: 15px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; }
            .stats b { color: var(--fucsia); font-size: 16px; }
            .input-group { position: relative; margin-bottom: 20px; }
            input { width: 100%; padding: 16px; border-radius: 12px; border: 2px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
            .btn-clear { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #222; color: #fff; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; font-weight: bold; }
            .btn-main { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
            .thumb { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 15px; }
            .support-msg { background: rgba(0, 242, 234, 0.05); color: #2ecc71; padding: 15px; border-radius: 15px; font-size: 13px; line-height: 1.5; border: 1px dashed #00f2ea; }
            .btn-dl { width: 100%; padding: 18px; background: #2ecc71; color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 17px; cursor: pointer; margin-top: 15px; text-decoration: none; display: block; }
            .btn-dl:disabled { background: #333; color: #777; cursor: not-allowed; }
            footer { margin-top: 40px; font-size: 11px; color: #444; }
            footer a { color: var(--cian); text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TurboLink</h1>
            <p style="font-size:10px; color:#666; margin-top:-10px;">PROPIEDAD DE TURBOLINK DIGITAL</p>
            <div class="stats">
                <div>YT/TikTok: <b id="p-count">-</b></div>
                <div>Social: <b id="s-count">-</b></div>
            </div>
            <div class="input-group">
                <input type="text" id="urlInput" placeholder="Pega el link aquí...">
                <button class="btn-clear" onclick="resetPage()">✕</button>
            </div>
            <button id="btnAction" class="btn-main" onclick="analyze()">Generar Descarga</button>
            <div id="status" style="margin-top:15px; font-weight:bold; color: var(--cian);"></div>

            <div id="previewSection">
                <img id="vThumb" class="thumb" src="">
                <div class="support-msg">
                    🚀 <b>¡Video Detectado!</b><br>
                    Estamos preparando tu descarga segura. <b>Te invitamos a visitar nuestros anuncios</b>; esto nos ayuda a mantener TurboLink Digital gratuito para ti. ¡Gracias!
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

            function resetPage() {
                document.getElementById('urlInput').value = '';
                document.getElementById('previewSection').style.display = 'none';
                document.getElementById('status').innerText = '';
                document.getElementById('btnAction').disabled = false;
            }

            async function analyze() {
                const url = document.getElementById('urlInput').value.trim(); if(!url) return;
                const status = document.getElementById('status');
                const preview = document.getElementById('previewSection');
                const btn = document.getElementById('btnAction');
                
                status.innerText = "⏳ Analizando enlace...";
                btn.disabled = true;

                try {
                    const r = await fetch('/api/get_info?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        status.innerText = "✅ Video Encontrado";
                        document.getElementById('vThumb').src = d.thumbnail;
                        // Protegemos el link en Base64 para evitar errores de transporte
                        document.getElementById('finalLink').href = "/player?v=" + btoa(d.download_url);
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
                                waitBtn.style.display = "none";
                                finalLink.style.display = "block";
                                getStats();
                            }
                        }, 1000);
                    } else { status.innerText = "❌ " + d.message; btn.disabled = false; }
                } catch(e) { status.innerText = "❌ Error de conexión."; btn.disabled = false; }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

@app.route('/api/get_info')
def get_info():
    raw_input = request.args.get('url', '')
    url = get_clean_url(raw_input)
    if not url: return jsonify({"success": False, "message": "Link no detectado."})

    ip = request.remote_addr
    stats = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and stats['premium'] <= 0) or (not is_p and stats['social'] <= 0):
        return jsonify({"success": False, "message": "Cupos diarios agotados."})

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
                "thumbnail": data.get('thumbnail') or data.get('picture') or ""
            })
    except: pass
    return jsonify({"success": False, "message": "Video no disponible."})

@app.route('/player')
def player():
    # Esta página emula el reproductor nativo para activar los 3 puntitos
    try:
        encoded_url = request.args.get('v')
        video_url = base64.b64decode(encoded_url).decode('utf-8')
        return render_template_string('''
        <html>
        <body style="margin:0; background:#000; display:flex; align-items:center; justify-content:center;">
            <video controls autoplay style="max-width:100%; max-height:100%;">
                <source src="/stream?v={{v}}" type="video/mp4">
            </video>
        </body>
        </html>
        ''', v=urllib.parse.quote_plus(video_url))
    except: return "Error al cargar video.", 400

@app.route('/stream')
def stream():
    # El túnel de Railway que evita el logueo de Facebook
    video_url = urllib.parse.unquote_plus(request.args.get('v'))
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(video_url, headers=headers, stream=True)
    return Response(stream_with_context(r.iter_content(chunk_size=1024*1024)), content_type='video/mp4')

@app.route('/privacidad')
def privacy(): return "<h1>Política de Privacidad - TurboLink Digital</h1>"

@app.route('/dmca')
def dmca(): return "<h1>DMCA - TurboLink Digital</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
