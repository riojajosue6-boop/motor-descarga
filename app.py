import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- DISEÑO PREMIUM CON SECCIONES LEGALES ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Descarga Pro | Bolivia</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        
        /* Navegación */
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; position: sticky; top: 0; z-index: 100; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; transition: 0.3s; }
        nav a:hover { color: var(--red); }

        /* Contenedores */
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 20px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        
        /* Elementos de Interfaz */
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; margin-bottom: 20px; outline: none; }
        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        
        /* Preview */
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }

        /* SECCIONES LEGALES (Ocultas por defecto) */
        .legal-content { display: none; text-align: left; background: #111; padding: 30px; border-radius: 15px; line-height: 1.6; color: #bbb; margin-top: 20px; border: 1px solid #222; }
        .legal-content h2 { color: #fff; border-bottom: 1px solid var(--red); padding-bottom: 10px; }
        
        .ad-slot { background: #111; border: 1px dashed #444; margin: 20px auto; padding: 15px; color: #444; font-size: 11px; }
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
            <div class="ad-slot">ESPACIO PUBLICIDAD SUPERIOR</div>
            <div class="main-card">
                <h1>🚀 MOTOR DE DESCARGA</h1>
                <input type="text" id="urlInput" placeholder="Pega el enlace de video aquí...">
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
            <div class="ad-slot">ESPACIO PUBLICIDAD INFERIOR</div>
        </div>

        <div id="privacy-sec" class="legal-content">
            <h2>Política de Privacidad</h2>
            <p>Última actualización: 19 de Marzo, 2026</p>
            <p>En <strong>Motor de Descarga Pro</strong>, accesible desde motor-descarga.onrender.com, una de nuestras principales prioridades es la privacidad de nuestros visitantes.</p>
            <p><strong>Archivos de registro:</strong> Seguimos un procedimiento estándar de uso de archivos de registro. Estos archivos registran a los visitantes cuando visitan sitios web. La información recopilada incluye direcciones IP, tipo de navegador, proveedor de servicios de Internet (ISP), fecha y hora, y páginas de referencia/salida.</p>
            <p><strong>Cookies y Web Beacons:</strong> Como cualquier otro sitio web, utilizamos 'cookies'. Estas cookies se utilizan para almacenar información, incluidas las preferencias de los visitantes y las páginas del sitio web a las que el visitante accedió o visitó.</p>
            <p><strong>Google DoubleClick DART Cookie:</strong> Google es uno de los proveedores externos en nuestro sitio. También utiliza cookies, conocidas como cookies de DART, para mostrar anuncios a los visitantes de nuestro sitio basándose en su visita a otros sitios en Internet.</p>
        </div>

        <div id="terms-sec" class="legal-content">
            <h2>Términos y Condiciones</h2>
            <p>Al acceder a este sitio web, asumimos que aceptas estos términos y condiciones en su totalidad.</p>
            <p><strong>Uso del Servicio:</strong> Este motor de descarga es una herramienta destinada únicamente para uso personal. El usuario es el único responsable de los contenidos descargados y de respetar los derechos de autor de las plataformas originales (YouTube, TikTok, etc.).</p>
            <p><strong>Restricciones:</strong> Está prohibido utilizar este sitio para descargar material protegido por derechos de autor con fines comerciales sin el permiso explícito del propietario del contenido.</p>
            <p><strong>Limitación de Responsabilidad:</strong> No almacenamos ningún video en nuestros servidores. Solo proporcionamos un puente técnico hacia el contenido alojado en las plataformas originales.</p>
        </div>
    </div>

    <footer>
        © 2026 Descargador Pro - Cochabamba | Hecho en Bolivia 🇧🇴
    </footer>

    <script>
        function showSection(sec) {
            document.getElementById('home-sec').style.display = sec === 'home' ? 'block' : 'none';
            document.getElementById('privacy-sec').style.display = sec === 'privacy' ? 'block' : 'none';
            document.getElementById('terms-sec').style.display = sec === 'terms' ? 'block' : 'none';
            window.scrollTo(0,0);
        }

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            if(!url) return alert("Pega un link");
            b.disabled = true;
            s.innerText = "⏳ Obteniendo miniatura...";
            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block';
                    s.innerText = "✅ Video listo para procesar";
                    document.getElementById('finalDownloadBtn').onclick = () => generateDownload(url, document.getElementById('formatInput').value);
                } else { s.innerText = "❌ Error al capturar info."; }
            } catch (e) { s.innerText = "❌ Error de conexión."; }
            b.disabled = false;
        }

        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            s.innerText = "🚀 Generando link final...";
            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                if(data.url) {
                    window.location.href = data.url;
                    s.innerText = "✅ Descarga iniciada";
                } else { s.innerText = "❌ No se pudo generar el link."; }
            } catch (e) { s.innerText = "❌ Error en el motor."; }
        }
    </script>
</body>
</html>
"""

# ... (El resto del código de las rutas API se mantiene igual que el anterior)
def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    if not url: return jsonify({"success": False})
    try:
        headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=15)
        data = r.json()
        thumb = data.get("thumbnail")
        if not thumb and ("youtube.com" in url or "youtu.be" in url):
            yid = get_yt_id(url)
            thumb = f"https://img.youtube.com/vi/{yid}/hqdefault.jpg"
        return jsonify({"success": True, "title": data.get("title", "Video"), "thumbnail": thumb})
    except: return jsonify({"success": False})

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"}
    try:
        if "youtube.com" in url or "youtu.be" in url:
            yid = get_yt_id(url)
            headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yid}, headers=headers, timeout=20)
            data = r.json()
            link = None
            if fmt == 'mp3':
                for f in data.get('adaptiveFormats', []):
                    if 'audio' in f.get('mimeType', ''): link = f.get('url'); break
            if not link:
                for f in data.get('formats', []):
                    if 'video' in f.get('mimeType', ''): link = f.get('url'); break
            return jsonify({"url": link or data.get('link')})
        else:
            headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, timeout=20)
            data = r.json()
            medias = data.get("medias", [])
            target = None
            if medias:
                for m in medias:
                    if fmt == 'mp3' and 'audio' in str(m.get('type')).lower(): target = m.get('url'); break
                    if fmt == 'mp4' and 'video' in str(m.get('type')).lower(): target = m.get('url'); break
                if not target: target = medias[0].get('url')
            return jsonify({"url": target})
    except: return jsonify({"error": "Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
