import os
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- DISEÑO PREMIUM OPTIMIZADO ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Motor de Descarga Pro | Bolivia</title>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8532381032470048" crossorigin="anonymous"></script>
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
        .clear-btn { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); background: #444; color: #fff; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }
        .clear-btn:hover { background: var(--red); }

        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }
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
        <div id="home-sec">
            <div class="main-card">
                <h1>🚀 MOTOR DE DESCARGA</h1>
                <div class="input-group">
                    <input type="text" id="urlInput" placeholder="Pega el enlace de video aquí...">
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
                    <img id="videoThumbnail" src="">
                    <div id="videoTitle" style="margin-top:10px; margin-bottom:15px; font-weight:bold; color:#fff;"></div>
                    <button id="finalDownloadBtn">CONFIRMAR DESCARGA</button>
                </div>
            </div>
        </div>

        <div id="privacy-sec" class="legal-content">
            <h2>Política de Privacidad</h2>
            <p>En <strong>Motor de Descarga Pro</strong>, valoramos tu privacidad...</p>
            <ul>
                <li><strong>Cookies:</strong> Usamos cookies para analítica y anuncios (Google AdSense).</li>
                <li><strong>Datos:</strong> No almacenamos tus archivos ni historial en nuestros servidores.</li>
            </ul>
        </div>

        <div id="terms-sec" class="legal-content">
            <h2>Términos y Condiciones</h2>
            <p>Al usar este sitio, aceptas:</p>
            <ul>
                <li>Uso personal y educativo bajo tu responsabilidad legal.</li>
                <li>Límite de duración de 10 minutos por video.</li>
            </ul>
        </div>
    </div>
    <footer>© 2026 Descargador Pro - Cochabamba 🇧🇴</footer>

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
            
            if(!url) return alert("Pega un link válido");
            b.disabled = true; s.innerText = "⏳ Analizando enlace de forma segura...";
            p.style.display = 'none';

            try {
                const res = await fetch(`/api/extract?url=${encodeURIComponent(url)}&type=${fmt}`);
                const data = await res.json();
                
                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; 
                    s.innerText = "✅ ¡Enlace generado!";
                    
                    // Acción de descarga forzada
                    document.getElementById('finalDownloadBtn').onclick = () => {
                        const link = document.createElement('a');
                        link.href = data.url;
                        link.target = '_blank';
                        link.setAttribute('download', ''); 
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    };
                } else {
                    s.innerText = "❌ Error: " + (data.error || "Video no disponible.");
                }
            } catch (e) { s.innerText = "❌ Error de conexión con el servidor."; }
            b.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/extract')
def api_extract():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    
    if not url:
        return jsonify({"success": False, "error": "URL no proporcionada"})

    # --- CONFIGURACIÓN REFORZADA DE YT-DLP ---
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        # Forzamos MP4 para video y M4A para audio (máxima compatibilidad)
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if fmt == 'mp4' else 'bestaudio[ext=m4a]/bestaudio',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True,
        'geo_bypass': True,
        # Filtro de seguridad: máximo 10 minutos (600 segundos)
        'match_filter': lambda info: None if info.get('duration', 0) <= 600 else 'Video muy largo (máximo 10 min)',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Intentar obtener la URL de descarga más directa
            link = info.get('url')
            if not link and 'formats' in info:
                # Filtrar formatos que tengan URL y elegir el último (suele ser el mejor)
                valid_formats = [f for f in info['formats'] if f.get('url')]
                if valid_formats:
                    link = valid_formats[-1]['url']

            if not link:
                return jsonify({"success": False, "error": "No se pudo extraer el enlace directo."})

            return jsonify({
                "success": True,
                "title": info.get('title', 'Video descargado'),
                "thumbnail": info.get('thumbnail'),
                "url": link
            })
    except Exception as e:
        # Personalizar el error del filtro de duración
        msg = str(e)
        if "Video muy largo" in msg:
            msg = "El video supera el límite de 10 minutos."
        return jsonify({"success": False, "error": msg})

if __name__ == "__main__":
    # Compatible con Render, Railway y despliegue local
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
