import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN MAESTRA ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
PROPIETARIO = "TurboLink Digital"
BLOG_CONTACTO = "https://tu-blog-aqui.blogspot.com" # Cambia por tu URL real

# Memoria de usuarios (Para producción real, se recomienda Redis, pero esto sirve para empezar)
user_data = {}

def get_clean_url(raw_url):
    url_match = re.search(r'(https?://[^\s]+)', raw_url)
    return url_match.group(1) if url_match else None

def get_user_stats(ip):
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_data or user_data.get(ip, {}).get('date') != today:
        user_data[ip] = {'date': today, 'premium': 2, 'social': 3}
    return user_data[ip]

# --- RUTAS PRINCIPALES ---

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TurboLink 🚀 | Reels & Shorts</title>
        <style>
            :root { --cian: #00f2ea; --fucsia: #ff0050; --bg: #050505; --card: #121212; }
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin:0; padding:15px; text-align:center; }
            .container { max-width: 500px; margin: auto; background: var(--card); padding: 25px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.1); }
            h1 { color: var(--cian); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 5px; text-shadow: 0 0 10px var(--cian); }
            .stats-bar { display: flex; justify-content: space-around; background: #1a1a1a; padding: 12px; border-radius: 12px; margin: 20px 0; font-size: 13px; border: 1px solid #222; }
            .stat-item b { color: var(--fucsia); font-size: 16px; }
            input { width: 100%; padding: 15px; border-radius: 12px; border: 2px solid #222; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; margin-bottom: 10px; }
            .btn-motor { width: 100%; padding: 16px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
            .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 15px; margin-top: 20px; font-weight: bold; }
            .dl-btn { background: #000; color: #fff; padding: 12px; text-decoration: none; border-radius: 8px; display: block; margin-top: 10px; }
            .footer { margin-top: 40px; font-size: 11px; color: #555; line-height: 1.6; }
            .footer a { color: var(--cian); text-decoration: none; }
            .alert-browser { display: none; background: var(--fucsia); color: #fff; padding: 12px; border-radius: 10px; margin-bottom: 15px; font-size: 13px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="browser-warning" class="alert-browser">⚠️ Estas en el navegador de una App. Para descargar con éxito, abre esta web en <b>CHROME</b>.</div>
            <h1>TurboLink</h1>
            <p style="font-size:10px; color:#666; margin-top:-10px;">PROPIEDAD DE TURBOLINK DIGITAL</p>

            <div class="stats-bar">
                <div class="stat-item">YT/TikTok: <b id="p-count">-</b></div>
                <div class="stat-item">Redes: <b id="s-count">-</b></div>
            </div>

            <div style="position:relative;">
                <input type="text" id="urlInput" placeholder="Pega el link de Reel o Short...">
                <button onclick="document.getElementById('urlInput').value=''" style="position:absolute; right:10px; top:12px; background:none; border:none; color:#555; font-size:20px;">×</button>
            </div>
            
            <button id="mainBtn" class="btn-motor" onclick="startProcess()">Generar Descarga</button>

            <div id="timer-box" style="display:none; margin-top:20px;">
                <p>🚀 Calentando motor... <span id="clock" style="color:var(--cian); font-size:25px;">15</span>s</p>
                <div style="border:1px solid #333; padding:10px; font-size:11px; color:#777;">La publicidad nos permite ser gratuitos.</div>
            </div>

            <div id="status"></div>
        </div>

        <div class="footer">
            <a href="/privacidad">Privacidad</a> | <a href="/dmca">DMCA</a> | <a href="{{ blog_url }}" target="_blank">Reclamos</a><br>
            © 2026 TurboLink Digital. <br> No alojamos archivos en nuestros servidores.
        </div>

        <script>
            // Actualizar contadores al cargar
            async function updateStats() {
                const r = await fetch('/api/stats');
                const d = await r.json();
                document.getElementById('p-count').innerText = d.premium;
                document.getElementById('s-count').innerText = d.social;
                if(d.premium <= 0 && d.social <= 0) {
                    document.getElementById('mainBtn').disabled = true;
                    document.getElementById('mainBtn').innerText = "Cupo Agotado";
                }
            }
            updateStats();

            async function startProcess() {
                const url = document.getElementById('urlInput').value;
                if(!url) return alert("Pega un link");
                
                const btn = document.getElementById('mainBtn');
                const timerBox = document.getElementById('timer-box');
                btn.disabled = true; timerBox.style.display = "block";
                
                let time = 15;
                let interval = setInterval(async () => {
                    time--; document.getElementById('clock').innerText = time;
                    if(time <= 0) {
                        clearInterval(interval);
                        timerBox.style.display = "none";
                        await fetchVideo(url);
                        btn.disabled = false;
                        updateStats();
                    }
                }, 1000);
            }

            async function fetchVideo(url) {
                const status = document.getElementById('status');
                status.innerHTML = "⏳ Extrayendo...";
                try {
                    const r = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        let html = `<div class="dl-box">✅ ¡LISTO!`;
                        if(d.type === 'tunnel') {
                            html += `<a href="/api/download?v=${encodeURIComponent(d.url)}" class="dl-btn">📥 GUARDAR TIKTOK</a>`;
                        } else {
                            html += `<a href="${d.url}" target="_blank" class="dl-btn">📥 DESCARGAR VIDEO</a>
                                    <div style="font-size:11px; margin-top:10px; color:#333;">⚠️ Si abre la App: Mantén presionado el botón y elige "Descargar vínculo"</div>`;
                        }
                        status.innerHTML = html + `</div>`;
                    } else { status.innerHTML = "❌ " + d.message; }
                } catch(e) { status.innerHTML = "❌ Error de conexión."; }
            }
        </script>
    </body>
    </html>
    ''', blog_url=BLOG_CONTACTO)

# --- API ENDPOINTS ---

@app.route('/api/stats')
def stats():
    s = get_user_stats(request.remote_addr)
    return jsonify(s)

@app.route('/api/fetch')
def fetch_api():
    raw_url = request.args.get('url')
    clean_url = get_clean_url(raw_url)
    if not clean_url: return jsonify({"success": False, "message": "Link inválido"})
    
    ip = request.remote_addr
    stats = get_user_stats(ip)
    
    is_premium = "tiktok.com" in clean_url or "youtube.com" in clean_url or "youtu.be" in clean_url
    
    if is_premium and stats['premium'] <= 0: return jsonify({"success": False, "message": "Sin cupos YT/TikTok"})
    if not is_premium and stats['social'] <= 0: return jsonify({"success": False, "message": "Sin cupos Redes"})

    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": clean_url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            if is_premium: stats['premium'] -= 1
            else: stats['social'] -= 1
            return jsonify({"success": True, "url": video_url, "type": "tunnel" if "tiktok.com" in clean_url else "direct"})
    except: pass
    return jsonify({"success": False, "message": "No se pudo obtener el video"})

@app.route('/api/download')
def tunnel():
    # El túnel para TikTok que protege tu 1GB limitando el peso
    v_url = request.args.get('v')
    r = requests.get(v_url, stream=True, timeout=20)
    def generate():
        total = 0
        for chunk in r.iter_content(chunk_size=1024*1024):
            total += len(chunk)
            if total > 15*1024*1024: break # Límite 15MB
            yield chunk
    return Response(stream_with_context(generate()), content_type='video/mp4', 
                    headers={'Content-Disposition': 'attachment; filename="TurboLink_Video.mp4"'})

# --- PÁGINAS LEGALES (ADSENSE READY) ---

@app.route('/privacidad')
def privacy():
    return f"""<body style="background:#000;color:#ccc;font-family:sans-serif;padding:30px;">
    <h1>Política de Privacidad</h1>
    <p>En {PROPIETARIO}, valoramos tu privacidad. No recolectamos nombres, correos ni datos personales.</p>
    <p><b>Cookies y Publicidad:</b> Utilizamos Google AdSense para mostrar anuncios. Google puede usar cookies para mostrar anuncios basados en tus visitas.</p>
    <p><b>Uso de IP:</b> Tu dirección IP se procesa únicamente para limitar las 5 descargas diarias por usuario.</p>
    <a href="/" style="color:cyan;">Volver</a></body>"""

@app.route('/dmca')
def dmca_page():
    return f"""<body style="background:#000;color:#ccc;font-family:sans-serif;padding:30px;">
    <h1>Aviso DMCA / Derechos de Autor</h1>
    <p>{PROPIETARIO} es una herramienta técnica que actúa como un puente (transcoding/proxy) para archivos públicos alojados en plataformas como TikTok, Facebook y YouTube.</p>
    <p><b>No Alojamientos:</b> No almacenamos ningún video en nuestros servidores. Todo el contenido es descargado directamente de los servidores de la plataforma de origen.</p>
    <p><b>Retirada de Contenido:</b> Si usted es dueño de un contenido y desea restringir su acceso, por favor contacte a la plataforma de origen donde el video está alojado.</p>
    <p>Consultas: Diríjase a nuestro <a href="{BLOG_CONTACTO}" style="color:cyan;">Blog de Soporte</a>.</p>
    <a href="/" style="color:cyan;">Volver</a></body>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
