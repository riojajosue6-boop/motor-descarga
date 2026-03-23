import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN DE ADS.TXT (Reemplaza con tu ID de editor de Google) ---
ADS_TXT_CONTENT = "google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0"

# --- DISEÑO PREMIUM CON ADSENSE Y CONTADOR ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Motor de Descarga Pro | Bolivia</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; position: sticky; top: 0; z-index: 100; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; transition: 0.3s; }
        nav a:hover { color: var(--red); }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        .input-group { position: relative; width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 18px 50px 18px 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; }
        .clear-btn { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); background: #444; color: #fff; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.3s; }
        .clear-btn:hover { background: var(--red); }
        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        
        /* ESPACIOS PARA ADSENSE */
        .ad-slot { background: #111; border: 1px dashed #444; margin: 20px 0; min-height: 90px; display: flex; align-items: center; justify-content: center; color: #555; font-size: 12px; }
        
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #videoTitle { margin-top: 10px; margin-bottom:15px; font-weight:bold; color:#fff; }
        
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: not-allowed; margin-top: 15px; opacity: 0.6; }
        .legal-content { display: none; text-align: left; background: #111; padding: 30px; border-radius: 15px; line-height: 1.6; color: #bbb; margin-top: 20px; border: 1px solid #222; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
    </head>
<body>
    <nav>
        <a onclick="showSection('home')">Inicio</a>
        <a onclick="showSection('privacy')">Privacidad</a>
        <a onclick="showSection('terms')">Términos</a>
    </nav>
    <div class="container">
        <div class="ad-slot">ANUNCIO SUPERIOR (AdSense)</div>

        <div id="home-sec">
            <div class="main-card">
                <h1>🚀 MOTOR DE DESCARGA</h1>
                <div class="input-group">
                    <input type="text" id="urlInput" placeholder="Pega el enlace de YouTube o TikTok aquí...">
                    <button class="clear-btn" onclick="clearUrl()">✕</button>
                </div>
                <div class="options">
                    <select id="formatInput">
                        <option value="mp4">🎬 Video MP4</option>
                        <option value="mp3">🎵 Audio MP3</option>
                    </select>
                </div>
                <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
                
                <div id="status" style="margin-top:20px; font-weight:bold;"></div>

                <div id="previewSection">
                    <div class="ad-slot">ANUNCIO INTERMEDIO (AdSense)</div>
                    <img id="videoThumbnail" src="">
                    <div id="videoTitle"></div>
                    <button id="finalDownloadBtn" disabled>ESPERA 5s...</button>
                </div>
            </div>
        </div>

        <div id="privacy-sec" class="legal-content">
            <h2>Política de Privacidad</h2>
            <p>En <strong>Motor de Descarga Pro</strong>, nos tomamos muy en serio tu privacidad. Esta política detalla cómo manejamos tus datos:</p>
            <ul>
                <li><strong>Cookies y AdSense:</strong> Google, como proveedor externo, utiliza cookies para publicar anuncios en nuestro sitio. El uso de la cookie de DART permite a Google mostrar anuncios basados en las visitas realizadas a este y otros sitios web.</li>
                <li><strong>Privacidad de Datos:</strong> No recopilamos nombres, correos electrónicos ni almacenamos los videos procesados. Nuestra herramienta actúa como un puente técnico efímero.</li>
                <li><strong>Analítica:</strong> Usamos herramientas de terceros para medir el tráfico de nuestro sitio de forma anónima.</li>
            </ul>
        </div>

        <div id="terms-sec" class="legal-content">
            <h2>Términos y Condiciones</h2>
            <p>Al acceder a nuestro sitio, aceptas cumplir con los siguientes términos de servicio:</p>
            <ul>
                <li><strong>Uso Personal:</strong> El servicio está destinado únicamente para el uso personal y educativo. No nos hacemos responsables por el uso que los usuarios den al material descargado.</li>
                <li><strong>Propiedad Intelectual:</strong> Respeta los derechos de autor. No utilices esta herramienta para piratear contenido protegido.</li>
                <li><strong>Restricciones:</strong> No se permite el procesamiento de videos que excedan los 10 minutos para preservar la estabilidad del sistema.</li>
            </ul>
        </div>
        
        <div class="ad-slot">ANUNCIO INFERIOR (AdSense)</div>
    </div>
    <footer>© 2026 Motor de Descarga Pro - Cochabamba 🇧🇴</footer>

    <script>
        function showSection(sec) {
            document.getElementById('home-sec').style.display = sec === 'home' ? 'block' : 'none';
            document.getElementById('privacy-sec').style.display = sec === 'privacy' ? 'block' : 'none';
            document.getElementById('terms-sec').style.display = sec === 'terms' ? 'block' : 'none';
        }

        function clearUrl() {
            document.getElementById('urlInput').value = "";
            document.getElementById('status').innerText = "";
            document.getElementById('previewSection').style.display = 'none';
        }

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const fmt = document.getElementById('formatInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            const dlBtn = document.getElementById('finalDownloadBtn');

            if(!url) return alert("Pega un link válido");
            
            b.disabled = true; 
            s.innerText = "⏳ Analizando enlace de forma segura...";
            p.style.display = 'none';

            try {
                const res = await fetch(`/api/extract?url=${encodeURIComponent(url)}&type=${fmt}`);
                const data = await res.json();

                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; 
                    s.innerText = "✅ ¡Enlace generado!";
                    
                    // Lógica del contador de 5 segundos
                    let timeLeft = 5;
                    dlBtn.disabled = true;
                    dlBtn.style.cursor = "not-allowed";
                    dlBtn.style.opacity = "0.6";
                    
                    const timer = setInterval(() => {
                        if(timeLeft <= 0) {
                            clearInterval(timer);
                            dlBtn.innerText = "CONFIRMAR DESCARGA";
                            dlBtn.disabled = false;
                            dlBtn.style.cursor = "pointer";
                            dlBtn.style.opacity = "1";
                            dlBtn.onclick = () => window.open(data.url, '_blank');
                        } else {
                            dlBtn.innerText = `ESPERA ${timeLeft}s...`;
                            timeLeft--;
                        }
                    }, 1000);

                } else {
                    s.innerText = "❌ Error: " + data.error;
                }
            } catch (e) { 
                s.innerText = "❌ Error de conexión con el servidor."; 
            }
            b.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

# --- RUTA PARA ADS.TXT ---
@app.route('/ads.txt')
def ads_txt():
    return Response(ADS_TXT_CONTENT, mimetype='text/plain')

@app.route('/api/extract')
def api_extract():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    
    if not url:
        return jsonify({"success": False, "error": "URL requerida"})

    # PROXIES RESIDENCIALES ROTATIVOS
    proxy_users = ["ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", "ksvyuzxs-9", "ksvyuzxs-10"]
    proxy_pass = "r148qqniiwdz"
    proxy_host = "p.webshare.io"
    proxy_port = "80"

    for user in proxy_users:
        proxy_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        
        ydl_opts = {
            'proxy': proxy_url,
            'quiet': True,
            'no_warnings': True,
            # Configuración de iPhone para TikTok y Android para YouTube
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
            'format': 'bestvideo+bestaudio/best' if fmt == 'mp4' else 'bestaudio/best',
            'nocheckcertificate': True,
            'geo_bypass': True,
            'match_filter': lambda info: None if info.get('duration', 0) <= 600 else 'Video muy largo (máx 10 min)',
            'add_header': ['Referer:https://www.google.com/', 'Origin:https://www.google.com/']
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                link = info.get('url')
                if not link and 'formats' in info:
                    valid_formats = [f for f in info['formats'] if f.get('url')]
                    if valid_formats:
                        link = valid_formats[-1]['url']
                
                if link:
                    return jsonify({
                        "success": True,
                        "title": info.get('title', 'Video Procesado'),
                        "thumbnail": info.get('thumbnail'),
                        "url": link
                    })
        except Exception as e:
            if "muy largo" in str(e):
                return jsonify({"success": False, "error": "El video excede los 10 min."})
            continue

    return jsonify({"success": False, "error": "Error de conexión con la plataforma. Reintente."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
