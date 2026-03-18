import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- PLANTILLA TODO-EN-UNO (DISEÑO + LÓGICA + LEGAL) ---
HTML_PRO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargador Pro - YouTube & TikTok</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; }
        body { background: var(--dark); color: #eee; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; }
        nav { background: #000; padding: 15px; text-align: center; border-bottom: 1px solid #333; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        nav a:hover { color: var(--red); }
        
        .ad-banner { background: #111; border: 1px dashed #333; margin: 20px auto; padding: 15px; max-width: 728px; text-align: center; color: #444; }
        
        .main-card { background: var(--gray); padding: 30px; border-radius: 20px; max-width: 500px; margin: 20px auto; border: 1px solid #333; box-shadow: 0 15px 35px rgba(0,0,0,0.7); text-align: center; }
        h1 { color: var(--red); margin: 0; font-size: 32px; }
        input { width: 90%; padding: 15px; margin: 20px 0; border-radius: 10px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; outline: none; }
        input:focus { border-color: var(--red); }
        
        .selectors { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; }
        select { padding: 12px; border-radius: 8px; background: #222; color: white; border: 1px solid #444; cursor: pointer; }
        
        button { width: 95%; padding: 16px; background: var(--red); color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 18px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #cc0000; transform: translateY(-2px); }
        button:disabled { background: #444; cursor: not-allowed; }
        
        #status { margin-top: 25px; min-height: 30px; font-weight: 600; }
        
        .legal-content { max-width: 800px; margin: 40px auto; padding: 20px; display: none; background: #111; border-radius: 10px; font-size: 14px; line-height: 1.6; color: #aaa; text-align: left; }
        footer { padding: 40px; text-align: center; color: #555; font-size: 12px; }
    </style>
</head>
<body>

    <nav>
        <a onclick="showPage('home')">Inicio</a>
        <a onclick="showPage('privacy')">Privacidad</a>
        <a onclick="showPage('terms')">Términos</a>
        <a href="mailto:tu-correo@gmail.com">Contacto</a>
    </nav>

    <div class="ad-banner">
        <small>PUBLICIDAD</small><br>
        </div>

    <div id="home-page">
        <div class="main-card">
            <h1>🚀 Descargador Pro</h1>
            <p style="color: #888;">Cochabamba - Servicio Gratuito</p>
            
            <input type="text" id="urlInput" placeholder="Pega el enlace de video aquí...">
            
            <div class="selectors">
                <select id="formatInput">
                    <option value="mp4">🎬 Video MP4</option>
                    <option value="mp3">🎵 Audio MP3</option>
                </select>
            </div>

            <button id="btnAction" onclick="countdown()">DESCARGAR AHORA</button>
            <div id="status"></div>
        </div>
    </div>

    <div id="privacy" class="legal-content">
        <h2>Política de Privacidad</h2>
        <p>En Descargador Pro, valoramos tu privacidad. No almacenamos los videos que descargas ni tus datos personales. El servicio utiliza APIs de terceros para procesar las solicitudes. Al usar este sitio, aceptas el uso de cookies para publicidad personalizada a través de Google AdSense.</p>
    </div>

    <div id="terms" class="legal-content">
        <h2>Términos de Servicio</h2>
        <p>Este sitio es una herramienta para descargar contenido de uso personal. No nos hacemos responsables del mal uso del material descargado. Asegúrate de tener los derechos del contenido que intentas bajar. Queda prohibida la descarga de material con derechos de autor protegidos para fines comerciales.</p>
    </div>

    <div class="ad-banner">
        <small>PUBLICIDAD</small><br>
        </div>

    <footer>
        © 2026 Motor de Descarga Cochabamba | Orgullosamente Boliviano 🇧🇴
    </footer>

    <script>
        function showPage(pageId) {
            document.getElementById('home-page').style.display = pageId === 'home' ? 'block' : 'none';
            document.getElementById('privacy').style.display = pageId === 'privacy' ? 'block' : 'none';
            document.getElementById('terms').style.display = pageId === 'terms' ? 'block' : 'none';
            window.scrollTo(0,0);
        }

        function countdown() {
            const url = document.getElementById('urlInput').value;
            const btn = document.getElementById('btnAction');
            const status = document.getElementById('status');
            const tipo = document.getElementById('formatInput').value;

            if(!url) return alert("Por favor pega un enlace válido.");

            btn.disabled = true;
            let timer = 5;

            const interval = setInterval(() => {
                status.style.color = "#ffcc00";
                status.innerText = `🔄 Preparando enlace en ${timer} segundos...`;
                timer--;

                if(timer < 0) {
                    clearInterval(interval);
                    processDownload(url, tipo);
                }
            }, 1000);
        }

        async function processDownload(url, tipo) {
            const status = document.getElementById('status');
            const btn = document.getElementById('btnAction');
            
            try {
                const res = await fetch(`/api/get?url=${encodeURIComponent(url)}&tipo=${tipo}`);
                const data = await res.json();

                if(data.link) {
                    status.style.color = "#00ff88";
                    status.innerText = "✅ ¡Enlace listo! Descargando...";
                    window.location.href = data.link;
                } else {
                    status.style.color = "#ff4444";
                    status.innerText = "❌ Error: " + (data.error || "No disponible");
                }
            } catch (e) {
                status.innerText = "❌ Error de conexión.";
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PRO)

@app.route('/api/get')
def get_api():
    u = request.args.get('url')
    t = request.args.get('tipo', 'mp4')
    if not u: return jsonify({"error": "No URL"}), 400
    
    u = u.split('?')[0].split('&')[0]
    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post("https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                          json={"url": u}, headers=headers, timeout=25)
        data = r.json()
        medias = data.get("medias", [])
        
        link = None
        if isinstance(medias, list):
            for m in medias:
                if t == 'mp3' and (m.get('type') == 'audio' or 'audio' in m.get('quality', '')):
                    link = m.get('url'); break
                if t == 'mp4' and 'video' in m.get('type', ''):
                    link = m.get('url'); break
            if not link and medias: link = medias[0].get('url')
        elif isinstance(medias, dict):
            for m in medias.values():
                if t == 'mp3' and (m.get('type') == 'audio' or 'audio' in m.get('quality', '')):
                    link = m.get('url'); break
                if t == 'mp4' and 'video' in m.get('type', ''):
                    link = m.get('url'); break
            if not link and medias: link = list(medias.values())[0].get('url')

        return jsonify({"link": link})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
