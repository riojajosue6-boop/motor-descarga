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
BLOG_CONTACTO = "https://tu-blog-aqui.blogspot.com" # Cambia esto por tu link real después

# Base de datos temporal (Se reinicia si el server duerme, ideal para pruebas)
user_data = {}

def get_clean_url(raw_url):
    """Extrae solo la URL limpia si el usuario pega texto extra"""
    url_match = re.search(r'(https?://[^\s]+)', raw_url)
    return url_match.group(1) if url_match else None

def get_user_stats(ip):
    """Inicializa o recupera los créditos del usuario"""
    today = datetime.now().strftime('%Y-%m-%d')
    if ip not in user_data or user_data[ip]['date'] != today:
        user_data[ip] = {
            'date': today,
            'premium_slots': 2, # YT y TikTok
            'social_slots': 3   # FB, IG, etc.
        }
    return user_data[ip]

# --- VISTA PRINCIPAL (DISEÑO NEÓN) ---
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
            body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin:0; padding:20px; text-align:center; }
            .container { max-width: 500px; margin: auto; background: var(--card); padding: 25px; border-radius: 20px; border: 1px solid #333; box-shadow: 0 0 20px rgba(0,242,234,0.1); }
            h1 { color: var(--cian); text-transform: uppercase; letter-spacing: 3px; margin-bottom: 5px; }
            .neon-text { text-shadow: 0 0 10px var(--cian); }
            
            .stats-bar { display: flex; justify-content: space-around; background: #1a1a1a; padding: 10px; border-radius: 10px; margin: 20px 0; font-size: 13px; }
            .stat-item b { color: var(--fucsia); }

            input { width: 100%; padding: 15px; border-radius: 12px; border: 2px solid #222; background: #000; color: #fff; box-sizing: border-box; font-size: 16px; margin-bottom: 10px; }
            input:focus { border-color: var(--cian); outline: none; }

            .btn-motor { width: 100%; padding: 15px; background: var(--cian); color: #000; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
            .btn-motor:disabled { background: #333; color: #666; cursor: not-allowed; }

            .footer-links { margin-top: 30px; font-size: 11px; color: #444; }
            .footer-links a { color: #666; text-decoration: none; margin: 0 10px; }
            
            .alert-browser { display: none; background: var(--fucsia); color: #fff; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-size: 12px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="browser-warning" class="alert-browser">⚠️ Estas en el navegador de una App. Para descargar, abre TurboLink en CHROME.</div>
            
            <h1 class="neon-text">TurboLink</h1>
            <p style="font-size:10px; color:#666; margin-top:-10px;">PROPIEDAD DE TURBOLINK DIGITAL</p>

            <div class="stats-bar">
                <div class="stat-item">YT/TikTok: <b id="count-premium">2/2</b></div>
                <div class="stat-item">Social: <b id="count-social">3/3</b></div>
            </div>

            <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            <button id="mainBtn" class="btn-motor" onclick="startProcess()">Generar Descarga</button>

            <div id="timer-msg" style="display:none; margin-top:15px;">
                <p>🚀 Procesando... <span id="countdown" style="color:var(--cian); font-weight:bold;">15</span>s</p>
                <small style="color:#666;">La publicidad mantiene este servicio gratis.</small>
            </div>

            <div id="status"></div>
        </div>

        <div class="footer-links">
            <a href="/privacidad">Privacidad</a> | 
            <a href="/dmca">DMCA</a> | 
            <a href="{{ blog_url }}" target="_blank">Reclamos (Blog)</a>
            <p>© 2026 TurboLink Digital. No alojamos contenido.</p>
        </div>

        <script>
            // DETECTOR DE NAVEGADOR INTERNO
            const ua = navigator.userAgent || navigator.vendor || window.opera;
            if ((ua.indexOf("FBAN") > -1) || (ua.indexOf("FBAV") > -1) || (ua.indexOf("Instagram") > -1)) {
                document.getElementById('browser-warning').style.display = 'block';
            }

            async function startProcess() {
                // ... Lógica de contador y llamada a API que completaremos en Fase 3
            }
        </script>
    </body>
    </html>
    ''', blog_url=BLOG_CONTACTO)

# --- RUTAS LEGALES ---
@app.route('/privacidad')
def privacidad():
    return f"<h1>Política de Privacidad - {PROPIETARIO}</h1><p>Solo procesamos IPs para límites diarios...</p>"

@app.route('/dmca')
def dmca():
    return f"<h1>Cumplimiento DMCA - {PROPIETARIO}</h1><p>TurboLink es una herramienta de tránsito...</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
