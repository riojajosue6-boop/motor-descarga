import os
import requests
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN DE PROXIES RESIDENCIALES ---
proxy_users = ["ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", "ksvyuzxs-9", "ksvyuzxs-10"]
proxy_pass = "r148qqniiwdz"
proxy_host = "p.webshare.io"
proxy_port = "80"

def get_proxy():
    user = proxy_users[0]
    proxy_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    return {"http": proxy_url, "https": proxy_url}

# --- DISEÑO PREMIUM (Sólido y Cerrado) ---
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
        .clear-btn { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); background: #444; color: #fff; border: none; border-radius: 50%; width: 25px; height: 25px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        .ad-slot { margin: 20px auto; min-height: 90px; border: 1px dashed #333; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #videoTitle { margin-top: 10px; margin-bottom:15px; font-weight:bold; color:#fff; }
        #supportBox { display: none; background: #1a2a1a; color: #99ff99; border: 1px solid #00aa00; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        #finalDownloadBtn:disabled { background: #333; color: #777; cursor: not-allowed; opacity: 0.6; }
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
            <div class="ad-slot">ANUNCIO SUPERIOR</div>
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
                    <div id="videoTitle"></div>
                    <div id="supportBox">
                        ❤️ <strong>Querido usuario:</strong> Apóyanos visitando las publicidades para mantener el servicio gratuito.
                        <span id="countdownText" style="display:block; margin-top:10px;">El botón se activará en 5...</span>
                    </div>
                    <button id="finalDownloadBtn" disabled>CONFIRMAR DESCARGA</button>
                </div>
            </div>
            <div class="ad-slot">ANUNCIO INFERIOR</div>
        </div>
        <div id="privacy-sec" class="legal-content">
            <h2>Política de Privacidad</h2>
            <p>Usamos cookies de AdSense. No almacenamos tus videos ni datos personales.</p>
        </div>
        <div id="terms-sec" class="legal-content">
            <h2>Términos y Condiciones</h2>
            <p>Uso personal y educativo. Respetamos los derechos de autor.</p>
        </div>
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
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            const box = document.getElementById('supportBox');
            const dBtn = document.getElementById('finalDownloadBtn');
            if(!url) return alert("Pega un link");
            b.disabled = true; p.style.display = 'none'; s.innerText = "⏳ Analizando...";
            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block'; box.style.display = 'block'; s.innerText = "✅ Detectado";
                    let timeLeft = 5;
                    dBtn.disabled = true;
                    const countdown = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `El botón se activará en ${timeLeft}...`;
                        if(timeLeft <= 0) {
                            clearInterval(countdown);
                            document.getElementById('countdownText').style.display = 'none';
                            dBtn.disabled = false;
                        }
                    }, 1000);
                    dBtn.onclick = () => generateDownload(url, document.getElementById('formatInput').value);
                } else { s.innerText = "❌ No detectado."; }
            } catch (e) { s.innerText = "❌ Error."; }
            b.disabled = false;
        }
        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            s.innerText = "🚀 Generando...";
            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                if(data.url) {
                    window.open(data.url, '_blank');
                    s.innerText = "✅ Iniciada";
                } else { s.innerText = "❌ Error de link."; }
            } catch (e) { s.innerText = "❌ Error servidor."; }
        }
    </script>
</body>
</html>
"""

def get_yt_id(url):
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"}
    
    try:
        # MÉTODO 1: YouTube Específico
        if "youtube.com" in url or "youtu.be" in url:
            yid = get_yt_id(url)
            headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yid}, headers=headers, proxies=get_proxy(), timeout=20)
            data = r.json()
            
            # Buscamos el mejor link disponible
            link = None
            f_list = data.get('adaptiveFormats', []) if fmt == 'mp3' else data.get('formats', [])
            for f in f_list:
                if fmt == 'mp3' and 'audio' in f.get('mimeType', ''): 
                    link = f.get('url')
                    break
                if fmt == 'mp4' and 'video' in f.get('mimeType', '') and f.get('url'): 
                    link = f.get('url')
                    break
            
            # Si el método 1 falló, probamos el link directo que a veces viene en 'link'
            final_url = link or data.get('link')
            if final_url:
                return jsonify({"url": final_url})

        # MÉTODO 2: Multiplataforma (TikTok, FB, etc) y respaldo de YT
        headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, proxies=get_proxy(), timeout=20)
        data = r.json()
        medias = data.get("medias", [])
        
        target = None
        for m in medias:
            m_type = str(m.get('type')).lower()
            if fmt == 'mp3' and 'audio' in m_type: 
                target = m.get('url')
                break
            if fmt == 'mp4' and 'video' in m_type: 
                target = m.get('url')
                break
        
        if not target and medias:
            target = medias[0].get('url')
            
        if target:
            return jsonify({"url": target})
        else:
            return jsonify({"error": "No se encontró un link de descarga válido"}), 404

    except Exception as e:
        print(f"Error en api_down: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/ads.txt')
def ads_txt():
    return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
