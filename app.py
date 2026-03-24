import os
import requests
import re
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

def get_proxy(index=0):
    user = proxy_users[index % len(proxy_users)]
    p_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    return {"http": p_url, "https": p_url}

# --- DISEÑO PREMIUM MULTIPLATAFORMA ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Motor de Descarga Pro | Bolivia (FB, IG, YT, TT)</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        .input-group { position: relative; width: 100%; margin-bottom: 20px; }
        input { width: 100%; padding: 18px 50px 18px 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; outline: none; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #supportBox { display: none; background: #1a2a1a; color: #99ff99; border: 1px solid #00aa00; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        #finalDownloadBtn:disabled { background: #333; color: #777; cursor: not-allowed; opacity: 0.6; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card">
            <h1>🚀 MOTOR DE DESCARGA</h1>
            <p style="color:#888; font-size:14px;">YouTube • TikTok • Facebook • Instagram</p>
            <div class="input-group">
                <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            </div>
            <select id="formatInput" style="width:100%; padding:15px; border-radius:10px; background:#222; color:white; margin-bottom:20px; border:1px solid #444;">
                <option value="mp4">🎬 Video MP4</option>
                <option value="mp3">🎵 Audio MP3 (YouTube)</option>
            </select>
            <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
            <div id="status" style="margin-top:20px; font-weight:bold;"></div>
            <div id="previewSection">
                <img id="videoThumbnail" src="" style="width:100%; max-width:400px; border-radius:15px;">
                <div id="videoTitle" style="margin-top:10px; font-weight:bold; color:#fff;"></div>
                <div id="supportBox">
                    ❤️ <strong>Apóyanos visitando las publicidades</strong> para mantener el servicio gratuito.
                    <span id="countdownText" style="display:block; margin-top:10px;">Activando botón en 5...</span>
                </div>
                <button id="finalDownloadBtn" disabled>DESCARGAR AHORA</button>
            </div>
        </div>
    </div>
    <script>
        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            if(!url) return alert("Pega un link");
            b.disabled = true; p.style.display = 'none'; s.innerText = "⏳ Analizando enlace...";
            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail || "";
                    document.getElementById('videoTitle').innerText = info.title || "Video Detectado";
                    p.style.display = 'block'; document.getElementById('supportBox').style.display = 'block';
                    s.innerText = "✅ ¡Enlace Procesado!";
                    let timeLeft = 5;
                    const dBtn = document.getElementById('finalDownloadBtn');
                    dBtn.disabled = true;
                    const countdown = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `Activando botón en ${timeLeft}...`;
                        if(timeLeft <= 0) { clearInterval(countdown); document.getElementById('countdownText').style.display = 'none'; dBtn.disabled = false; }
                    }, 1000);
                    dBtn.onclick = () => generateDownload(url, document.getElementById('formatInput').value);
                } else { s.innerText = "❌ Error: Link bloqueado o inválido."; }
            } catch (e) { s.innerText = "❌ Error de servidor."; }
            b.disabled = false;
        }
        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            s.innerText = "🚀 Generando enlace final...";
            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                if(data.url) { window.open(data.url, '_blank'); s.innerText = "✅ Descarga lista"; }
                else { s.innerText = "❌ No se pudo generar el archivo."; }
            } catch (e) { s.innerText = "❌ Error en la descarga."; }
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

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    if not url: return jsonify({"success": False})
    for i in range(3):
        try:
            headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, proxies=get_proxy(i), timeout=12)
            data = r.json()
            if data.get("title") or data.get("thumbnail"):
                return jsonify({"success": True, "title": data.get("title"), "thumbnail": data.get("thumbnail")})
        except: continue
    return jsonify({"success": False})

@app.route('/api/down')
def api_down():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    for i in range(3):
        try:
            headers = {"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"}
            if "youtube.com" in url or "youtu.be" in url:
                yid = get_yt_id(url)
                headers["x-rapidapi-host"] = "yt-api.p.rapidapi.com"
                r = requests.get("https://yt-api.p.rapidapi.com/dl", params={"id": yid}, headers=headers, proxies=get_proxy(i), timeout=15)
                data = r.json()
                formats = data.get('adaptiveFormats', []) if fmt == 'mp3' else data.get('formats', [])
                for f in formats:
                    if (fmt == 'mp3' and 'audio' in f.get('mimeType', '')) or (fmt == 'mp4' and 'video' in f.get('mimeType', '')):
                        return jsonify({"url": f.get('url')})
            
            headers["x-rapidapi-host"] = "download-all-in-one-lite.p.rapidapi.com"
            r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", params={"url": url}, headers=headers, proxies=get_proxy(i), timeout=15)
            data = r.json()
            medias = data.get("medias", [])
            for m in medias:
                m_type = str(m.get('type')).lower()
                if (fmt == 'mp4' and 'video' in m_type) or (fmt == 'mp3' and 'audio' in m_type):
                    return jsonify({"url": m.get('url')})
            if medias: return jsonify({"url": medias[0].get('url')})
        except: continue
    return jsonify({"error": "No link"}), 500

@app.route('/ads.txt')
def ads_txt():
    return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
