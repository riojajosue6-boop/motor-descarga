import os
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- TU DISEÑO PREMIUM ORIGINAL (CON BOTÓN LIMPIAR Y TEXTOS LEGALES INTACTOS) ---
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
        
        /* --- ESTILO DEL INPUT Y BOTÓN LIMPIAR --- */
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
                    <div id="videoTitle" style="margin-bottom:15px; font-weight:bold; color:#fff;"></div>
                    <button id="finalDownloadBtn">CONFIRMAR DESCARGA</button>
                </div>
            </div>
        </div>

        <div id="privacy-sec" class="legal-content">
            <h2>Política de Privacidad</h2>
            <p>En <strong>Motor de Descarga Pro</strong>, valoramos tu privacidad. Esta política describe cómo manejamos la información:</p>
            <ul>
                <li><strong>Cookies:</strong> Utilizamos cookies para personalizar anuncios y analizar nuestro tráfico. Compartimos información sobre el uso que haces de nuestro sitio con nuestros partners de publicidad y análisis web como Google AdSense.</li>
                <li><strong>Google AdSense:</strong> Como proveedor externo, Google utiliza cookies para publicar anuncios en este sitio basados en tus visitas anteriores. Puedes inhabilitar el uso de la cookie de publicidad personalizada visitando Preferencias de anuncios de Google.</li>
                <li><strong>Datos de Usuario:</strong> No almacenamos los videos que descargas ni conservamos registros personales de tus búsquedas. Nuestra herramienta funciona como un puente técnico temporal.</li>
            </ul>
        </div>

        <div id="terms-sec" class="legal-content">
            <h2>Términos y Condiciones</h2>
            <p>Al utilizar este sitio, aceptas los siguientes términos:</p>
            <ul>
                <li><strong>Uso Responsable:</strong> Esta herramienta está diseñada para descargar contenido de uso personal y educativo. El usuario es el único responsable por el respeto a los derechos de autor de los videos descargados.</li>
                <li><strong>Sin Garantías:</strong> No garantizamos que el servicio sea ininterrumpido. El acceso a ciertas plataformas (como YouTube) puede verse limitado por cambios técnicos ajenos a nuestra voluntad.</li>
                <li><strong>Limitación de Responsabilidad:</strong> No nos hacemos responsables por el uso indebido del material descargado ni por daños técnicos derivados del uso de la herramienta.</li>
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
            
            if(!url) return alert("Pega un link");
            b.disabled = true; s.innerText = "⏳ Analizando enlace de forma segura...";
            p.style.display = 'none';

            try {
                const res = await fetch(`/api/extract?url=${encodeURIComponent(url)}&type=${fmt}`);
                const data = await res.json();
                
                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; s.innerText = "✅ ¡Enlace generado!";
                    document.getElementById('finalDownloadBtn').onclick = () => window.open(data.url, '_blank');
                } else {
                    s.innerText = "❌ Error: Plataforma bloqueada o video muy largo.";
                }
            } catch (e) { s.innerText = "❌ Error de conexión."; }
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
    
    # --- CAMUFLAJE Y SEGURIDAD REFORZADA ---
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best' if fmt == 'mp4' else 'bestaudio/best',
        # Cabeceras para simular ser un humano con Chrome
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'nocheckcertificate': True,
        'geo_bypass': True,
        # Límite de seguridad de 10 minutos (600 segundos)
        'match_filter': lambda info: None if info.get('duration', 0) <= 600 else 'Video muy largo',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link = info.get('url')
            if not link and 'formats' in info:
                link = info['formats'][-1]['url']

            return jsonify({
                "success": True,
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "url": link
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
