import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN TURBOLINK DIGITAL ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_SOPORTE = "https://tu-blog-aqui.blogspot.com"

# Registro de límites por IP
user_registry = {}

def get_clean_url(raw_url):
    match = re.search(r'(https?://[^\s]+)', raw_url)
    return match.group(1) if match else None

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
            .support-msg { background: rgba(0, 242, 234, 0.05); color: #2ecc71; padding: 15px; border-radius: 15px; font-size: 13px; line-height: 1.5; border: 1px dashed #00f2ea; }
            .btn-dl { width: 100%; padding: 18px; background: #2ecc71; color: #000; border: none; border-radius: 12px; font-weight: bold; font-size: 17px; cursor: pointer; margin-top: 15px; text-decoration: none; display: block; }
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
            <div class="input-group">
                <input type="text" id="urlInput" placeholder="Pega el link aquí...">
                <button class="btn-clear" onclick="resetAll()">✕</button>
            </div>
            <button id="btnAction" class="btn-main" onclick="analyze()">Generar Descarga</button>
            <div id="status" style="margin-top:15px; font-weight:bold; color: var(--cian);"></div>

            <div id="previewSection">
                <img id="vThumb" class="thumb" src="">
                <div id="vTitle" style="font-weight:bold; font-size:14px; margin-bottom:15px;"></div>
                <div class="support-msg">
                    🚀 <b>¡Video Detectado!</b><br>
                    Mientras esperas, <b>visita nuestros anuncios</b> para apoyar a TurboLink Digital. Gracias a ti seguimos siendo gratuitos.
                    <br><br>
                    <span id="timerText" style="color:#fff; font-size:18px; font-weight:bold;">Activando en 12s...</span>
                </div>
                <a id="vLink" href="" download class="btn-dl" style="display:none;">DESCARGAR VIDEO</a>
                <button id="dlBtnPlaceholder" class="btn-dl" disabled>DESCARGAR VIDEO</button>
            </div>
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
                
                btn.disabled = true; status.innerText = "⏳ Procesando...";
                preview.style.display = 'none';

                try {
                    const r = await fetch('/api/get_info?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        status.innerText = "✅ ¡Listo!";
                        document.getElementById('vThumb').src = d.thumbnail;
                        document.getElementById('vTitle').innerText = d.title;
                        
                        const linkReal = document.getElementById('vLink');
                        linkReal.href = d.download_url;
                        
                        preview.style.display = 'block';

                        let timeLeft = 12;
                        const dlBtnPlace = document.getElementById('dlBtnPlaceholder');
                        const timerText = document.getElementById('timerText');
                        
                        const timer = setInterval(() => {
                            timeLeft--;
                            timerText.innerText = `Activando en ${timeLeft}s...`;
                            if(timeLeft <= 0) {
                                clearInterval(timer);
                                timerText.innerText = "¡Listo!";
                                dlBtnPlace.style.display = 'none';
                                linkReal.style.display = 'block';
                                getStats();
                            }
                        }, 1000);
                    } else { status.innerText = "❌ " + d.message; btn.disabled = false; }
                } catch(e) { status.innerText = "❌ Error de servidor."; btn.disabled = false; }
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
    url = get_clean_url(request.args.get('url'))
    if not url: return jsonify({"success": False, "message": "Link inválido."})
    
    ip = request.remote_addr
    st = check_user(ip)
    is_p = any(x in url for x in ["tiktok", "youtube", "youtu.be"])
    
    if (is_p and st['premium'] <= 0) or (not is_p and st['social'] <= 0):
        return jsonify({"success": False, "message": "Sin créditos diarios."})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST, "Content-Type": "application/json"}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        data = r.json()
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        if dl_url:
            if is_p: st['premium'] -= 1
            else: st['social'] -= 1
            return jsonify({
                "success": True, "download_url": dl_url, 
                "thumbnail": data.get('thumbnail') or data.get('picture') or "https://via.placeholder.com/400x200", 
                "title": data.get("title", "Video Detectado")
            })
    except: pass
    return jsonify({"success": False, "message": "Video no disponible."})

if __name__ == "__main__":
    # Puerto obligatorio para Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
