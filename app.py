import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"

user_registry = {}

def get_clean_url(raw_url):
    """
    EXTRACTOR BLINDADO: 
    Busca estrictamente algo que empiece con http y tenga formato de link.
    Ignora textos como 'attributeStyleMap', 'StylePropertyMap', etc.
    """
    # Esta expresión regular busca solo la URL limpia dentro de cualquier texto
    url_match = re.search(r'(https?://[^\s\'"<>]+)', raw_url)
    if url_match:
        clean = url_match.group(1)
        # Filtro de seguridad adicional para redes sociales
        if any(x in clean for x in ['facebook.com', 'fb.watch', 'tiktok.com', 'instagram.com', 'youtube.com', 'youtu.be']):
            return clean
    return None

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
        <title>TurboLink 🚀 | Descargas Reales</title>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; --card: #121212; }
            body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }
            .card { max-width: 450px; margin: 20px auto; background: var(--card); padding: 25px; border-radius: 25px; border: 1px solid #333; }
            h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 10px var(--cian); }
            .stats { display: flex; justify-content: space-around; font-size: 12px; margin: 15px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; border: 1px solid #333; }
            .stats b { color: var(--fucsia); font-size: 16px; }
            input { width: 100%; padding: 16px; border-radius: 12px; border: 2px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; margin-bottom: 10px; }
            .btn-main { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
            .thumb { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 15px; }
            .support-msg { background: rgba(0, 242, 234, 0.1); color: #2ecc71; padding: 15px; border-radius: 15px; font-size: 13px; line-height: 1.5; border: 1px dashed #00f2ea; margin-bottom: 15px;}
            .btn-dl { width: 100%; padding: 18px; background: #2ecc71; color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 17px; cursor: pointer; text-decoration: none; display: block; }
            .btn-dl:disabled { background: #333; color: #777; cursor: not-allowed; }
            footer { margin-top: 40px; font-size: 11px; color: #444; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TurboLink</h1>
            <div class="stats">
                <div>YT/TikTok: <b id="p-count">-</b></div>
                <div>Social: <b id="s-count">-</b></div>
            </div>
            <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            <button id="btnAction" class="btn-main" onclick="analyze()">GENERAR DESCARGA</button>
            <div id="status" style="margin-top:15px; font-weight:bold; color: var(--cian);"></div>

            <div id="previewSection">
                <img id="vThumb" class="thumb" src="">
                <div class="support-msg">
                    🚀 <b>¡Video Detectado!</b><br>
                    Ayúdanos visitando la publicidad. Tu descarga se habilitará en segundos.
                    <br><br>
                    <span id="timerText" style="color:#fff; font-size:18px; font-weight:bold;">Esperando 12s...</span>
                </div>
                <a id="finalLink" href="" class="btn-dl" style="display:none;" target="_blank">DESCARGAR VIDEO</a>
                <button id="waitBtn" class="btn-dl" disabled>DESCARGAR VIDEO</button>
            </div>
        </div>
        <footer>© 2026 TurboLink Digital</footer>

        <script>
            async function analyze() {
                const url = document.getElementById('urlInput').value.trim(); if(!url) return;
                const status = document.getElementById('status');
                const preview = document.getElementById('previewSection');
                const btn = document.getElementById('btnAction');
                
                status.innerText = "⏳ Limpiando y Analizando...";
                btn.disabled = true;

                try {
                    const r = await fetch('/api/get_info?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        status.innerText = "✅ Video Encontrado";
                        document.getElementById('vThumb').src = d.thumbnail;
                        // Abrimos el reproductor nativo como en tu foto de WhatsApp
                        document.getElementById('finalLink').href = "/player?v=" + encodeURIComponent(d.download_url);
                        preview.style.display = 'block';

                        let timeLeft = 12;
                        const waitBtn = document.getElementById('waitBtn');
                        const finalLink = document.getElementById('finalLink');
                        const timerText = document.getElementById('timerText');
                        
                        const timer = setInterval(() => {
                            timeLeft--;
                            timerText.innerText = `Esperando ${timeLeft}s...`;
                            if(timeLeft <= 0) {
                                clearInterval(timer);
                                timerText.innerText = "¡Listo!";
                                waitBtn.style.display = "none";
                                finalLink.style.display = "block";
                            }
                        }, 1000);
                    } else { status.innerText = "❌ " + d.message; btn.disabled = false; }
                } catch(e) { status.innerText = "❌ Error de conexión."; btn.disabled = false; }
            }

            async function getStats() {
                try {
                    const r = await fetch('/api/user_info');
                    const d = await r.json();
                    document.getElementById('p-count').innerText = d.premium;
                    document.getElementById('s-count').innerText = d.social;
                } catch(e){}
            }
            getStats();
        </script>
    </body>
    </html>
    ''')

@app.route('/player')
def player():
    video_url = request.args.get('v')
    return render_template_string('''
    <body style="margin:0; background:#000; display:flex; align-items:center; justify-content:center;">
        <video controls autoplay style="max-width:100%; max-height:100%;">
            <source src="/stream?v={{v}}" type="video/mp4">
        </video>
    </body>
    ''', v=video_url)

@app.route('/stream')
def stream():
    video_url = request.args.get('v')
    # Identidad de navegador para evitar el bloqueo de Facebook
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    r = requests.get(video_url, headers=headers, stream=True)
    return Response(stream_with_context(r.iter_content(chunk_size=1024*512)), content_type='video/mp4')

@app.route('/api/get_info')
def get_info():
    raw_input = request.args.get('url', '')
    url = get_clean_url(raw_input)
    
    if not url:
        return jsonify({"success": False, "message": "Link no válido."})

    headers = {
        "x-rapidapi-key": API_KEY, 
        "x-rapidapi-host": API_HOST, 
        "Content-Type": "application/json"
    }
    try:
        # Petición POST a tu API Pro
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        data = r.json()
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        if dl_url:
            return jsonify({
                "success": True, 
                "download_url": dl_url, 
                "thumbnail": data.get('thumbnail') or data.get('picture') or ""
            })
    except: pass
    return jsonify({"success": False, "message": "Video privado o no encontrado."})

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
