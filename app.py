import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN DE TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_SOPORTE = "https://tu-blog-aqui.blogspot.com"

# Registro de cuotas por IP (Se reinicia cada día)
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
        <title>TurboLink 🚀 | Descargador Pro</title>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; }
            body { background: var(--bg); color: white; font-family: sans-serif; margin:0; padding:15px; text-align:center; }
            .card { max-width: 450px; margin: auto; background: #121212; padding: 25px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.1); }
            h1 { color: var(--cian); text-transform: uppercase; text-shadow: 0 0 8px var(--cian); margin-bottom: 5px; }
            .stats { display: flex; justify-content: space-around; font-size: 13px; margin: 20px 0; background: #1a1a1a; padding: 12px; border-radius: 12px; border: 1px solid #222; }
            .stats b { color: var(--fucsia); font-size: 16px; }
            
            .input-group { position: relative; margin-bottom: 15px; }
            input { width: 100%; padding: 16px; border-radius: 12px; border: 2px solid #333; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
            .btn-clear { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #222; color: #fff; border: none; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; font-weight: bold; }
            
            .btn-main { width: 100%; padding: 18px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            #loader { display: none; margin-top: 20px; color: var(--cian); font-weight: bold; }
            
            #previewSection { display: none; margin-top: 25px; border-top: 1px solid #333; padding-top: 20px; }
            .thumb { width: 100%; border-radius: 15px; border: 1px solid #444; margin-bottom: 10px; }
            .support-msg { background: rgba(46, 204, 113, 0.1); color: #2ecc71; padding: 15px; border-radius: 12px; font-size: 13px; margin: 15px 0; border: 1px dashed #2ecc71; line-height: 1.4; }
            
            .btn-dl { width: 100%; padding: 16px; background: #2ecc71; color: #000; border: none; border-radius: 12px; font-weight: bold; text-decoration: none; display: block; margin-top: 10px; font-size: 16px; }
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
                <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
                <button class="btn-clear" onclick="resetPage()">✕</button>
            </div>

            <button id="btnAction" class="btn-main" onclick="startProcess()">Analizar Video</button>
            
            <div id="loader">🚀 Conectando... <span id="clock">12</span>s</div>

            <div id="previewSection">
                <img id="vThumb" class="thumb" src="">
                <div id="vTitle" style="font-weight:bold; font-size:14px; margin-bottom:10px;"></div>
                <div class="support-msg">
                    🚀 ¡Video detectado! Tu descarga se activará en breve. Gracias por apoyar este proyecto gratuito de <b>TurboLink Digital</b> haciendo clic en nuestros anuncios.
                    <br><br>
                    <span id="timerText" style="color:#fff; font-size:16px;">Esperando 12s...</span>
                </div>
                <a id="vLink" href="" target="_blank" style="text-decoration:none;">
                    <button id="dlBtn" class="btn-dl" disabled>DESCARGAR VIDEO</button>
                </a>
            </div>
            
            <div id="status" style="margin-top:15px; color:var(--fucsia); font-weight:bold;"></div>
        </div>
        <footer>
            <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a> | <a href="{{blog}}" target="_blank">Soporte</a>
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
                document.getElementById('loader').style.display = 'none';
                document.getElementById('btnAction').disabled = false;
            }

            async function startProcess() {
                const url = document.getElementById('urlInput').value;
                if(!url) return alert("Pega un link");
                
                const btn = document.getElementById('btnAction');
                const loader = document.getElementById('loader');
                document.getElementById('previewSection').style.display = 'none';
                document.getElementById('status').innerText = '';

                btn.disabled = true;
                loader.style.display = "block";
                
                let t = 12;
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
                        document.getElementById('dlBtn').disabled = false;
                    } else {
                        status.innerText = "❌ " + d.message;
                    }
                } catch(e) { status.innerText = "❌ Error de API."; }
            }
        </script>
    </body>
    </html>
    ''', blog=BLOG_SOPORTE)

@app.route('/api/user_info')
def user_info():
    return jsonify(check_user(request.remote_addr))

@app.route('/api/get_info')
def get_info():
    url = get_clean_url(request.args.get('url'))
    ip = request.remote_addr
    stats = check_user(ip)
    
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    if (is_p and stats['premium'] <= 0) or (not is_p and stats['social'] <= 0):
        return jsonify({"success": False, "message": "Sin créditos diarios."})

    # CONFIGURACIÓN DEL POST SEGÚN TU CURL
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
        "Content-Type": "application/json"
    }
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        data = r.json()
        
        # Extracción de link y miniatura (thumbnail) de tu API específica
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        thumb = data.get('thumbnail') or data.get('picture')

        if dl_url:
            if is_p: stats['premium'] -= 1
            else: stats['social'] -= 1
            return jsonify({
                "success": True, 
                "download_url": dl_url, 
                "thumbnail": thumb or "https://via.placeholder.com/400x200?text=TurboLink+Digital", 
                "title": data.get("title", "Video Listo")
            })
    except: pass
    return jsonify({"success": False, "message": "Video no disponible o enlace inválido."})

@app.route('/privacidad')
def privacy():
    return "<h1>Privacidad - TurboLink Digital</h1><p>Usamos tu IP para gestionar las 5 descargas diarias.</p>"

@app.route('/dmca')
def dmca_page():
    return "<h1>DMCA - TurboLink Digital</h1><p>Esta herramienta procesa enlaces externos públicos y no aloja contenido.</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
