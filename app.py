import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN DE PROXIES ---
proxy_users = ["ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", "ksvyuzxs-9", "ksvyuzxs-10"]
proxy_pass = "r148qqniiwdz"
proxy_host = "p.webshare.io"
proxy_port = "80"

def get_proxy(index=0):
    user = proxy_users[index % len(proxy_users)]
    p_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    return {"http": p_url, "https": p_url}

# --- DISEÑO PREMIUM FIEL A TUS CAPTURAS ---
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
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        .input-group { position: relative; width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 18px 50px 18px 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #supportBox { display: none; background: #1a2a1a; color: #99ff99; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #finalDownloadBtn { width: 100%; padding: 18px; background: #00aa00; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        #finalDownloadBtn:disabled { background: #333; cursor: not-allowed; opacity: 0.6; }
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
                <p style="color:#666; font-size:12px; margin-bottom:15px;">FB • IG • YT • TT</p>
                <div class="input-group">
                    <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
                </div>
                <select id="formatInput" style="width:100%; padding:15px; border-radius:10px; background:#222; color:white; border:1px solid #444; margin-bottom:20px;">
                    <option value="mp4">🎬 Video MP4</option>
                    <option value="mp3">🎵 Audio MP3</option>
                </select>
                <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
                <div id="status" style="margin-top:20px; font-weight:bold;"></div>
                <div id="previewSection">
                    <img id="videoThumbnail" src="">
                    <div id="videoTitle" style="margin-top:10px; font-weight:bold; color:#fff;"></div>
                    <div id="supportBox">
                        ❤️ <strong>Apóyanos visitando las publicidades</strong> para mantener el servicio gratuito.
                        <span id="countdownText" style="display:block; margin-top:10px;">El botón se activará en 5...</span>
                    </div>
                    <button id="finalDownloadBtn" disabled>CONFIRMAR DESCARGA</button>
                </div>
            </div>
        </div>
        <div id="privacy-sec" class="legal-content">
            <h2>Privacidad</h2><p>No almacenamos tus datos.</p>
        </div>
        <div id="terms-sec" class="legal-content">
            <h2>Términos</h2><p>Uso bajo responsabilidad del usuario.</p>
        </div>
    </div>
    <footer>© 2026 Motor de Descarga Pro - Cochabamba 🇧🇴</footer>
    <script>
        function showSection(sec) {
            document.getElementById('home-sec').style.display = sec === 'home' ? 'block' : 'none';
            document.getElementById('privacy-sec').style.display = sec === 'privacy' ? 'block' : 'none';
            document.getElementById('terms-sec').style.display = sec === 'terms' ? 'block' : 'none';
        }

        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const fmt = document.getElementById('formatInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            if(!url) return alert("Pega un link");
            
            b.disabled = true; p.style.display = 'none'; s.innerText = "⏳ Analizando enlace...";
            
            try {
                const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
                const data = await res.json();
                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; document.getElementById('supportBox').style.display = 'block';
                    s.innerText = "✅ ¡Detectado!";
                    
                    let timeLeft = 5;
                    const dBtn = document.getElementById('finalDownloadBtn');
                    dBtn.disabled = true;
                    dBtn.innerText = "ESPERE...";
                    
                    const timer = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `Activando en ${timeLeft}...`;
                        if(timeLeft <= 0) {
                            clearInterval(timer);
                            document.getElementById('countdownText').style.display = 'none';
                            dBtn.disabled = false;
                            dBtn.innerText = "CONFIRMAR DESCARGA";
                        }
                    }, 1000);

                    dBtn.onclick = async () => {
                        s.innerText = "🚀 Generando descarga...";
                        const resD = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${fmt}`);
                        const dataD = await resD.json();
                        if(dataD.url) {
                            window.location.href = dataD.url;
                            s.innerText = "✅ Descarga iniciada";
                        } else { s.innerText = "❌ Error al generar link."; }
                    };
                } else { s.innerText = "❌ Error: Enlace bloqueado o no detectado."; }
            } catch (e) { s.innerText = "❌ Error de servidor."; }
            b.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PREMIUM)

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    if not url: return jsonify({"success": False})
    # Usamos la API All-in-one con tus proxies como puente
    headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}
    try:
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, proxies=get_proxy(0), timeout=15)
        data = r.json()
        return jsonify({"success": True, "title": data.get("title", "Video"), "thumbnail": data.get("thumbnail", "")})
    except: return jsonify({"success": False})

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"}
    try:
        # Lógica YouTube
        if "youtube.com" in url or "youtu.be" in url:
            headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
            v_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url).group(1)
            r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": v_id}, headers=headers, proxies=get_proxy(1), timeout=15)
            data = r.json()
            formats = data.get('adaptiveFormats', []) if fmt == 'mp3' else data.get('formats', [])
            link = next((f['url'] for f in formats if (fmt == 'mp3' and 'audio' in f['mimeType']) or (fmt == 'mp4' and 'video' in f['mimeType'])), data.get('link'))
            return jsonify({"url": link})
        # Lógica Otros (FB, IG, TT)
        headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, proxies=get_proxy(2), timeout=15)
        data = r.json()
        link = next((m['url'] for m in data.get('medias', []) if (fmt == 'mp3' and 'audio' in str(m['type']).lower()) or (fmt == 'mp4' and 'video' in str(m['type']).lower())), data.get('medias', [{}])[0].get('url'))
        return jsonify({"url": link})
    except: return jsonify({"url": None})

@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
