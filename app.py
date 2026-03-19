import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- PLANTILLA HTML PREMIUM ---
HTML_PREMIUM = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Descargador Pro | Bolivia</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; padding: 0; text-align: center; }
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; display: inline-block; border: 1px solid #333; max-width: 550px; width: 90%; margin: 20px auto; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); margin: 0 0 10px 0; font-size: 32px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; font-size: 16px; box-sizing: border-box; margin-bottom: 20px; }
        .options { display: flex; gap: 10px; margin-bottom: 25px; }
        select { padding: 15px; border-radius: 10px; background: #222; color: white; border: 1px solid #444; flex: 1; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; border-radius: 15px; margin-bottom: 15px; }
        #finalDownloadBtn { width: 100%; padding: 15px; background: #00aa00; color: white; border: none; border-radius: 10px; font-weight: bold; text-decoration: none; display: inline-block; }
        .ad-slot { background: #111; border: 1px dashed #444; margin: 20px auto; padding: 10px; max-width: 728px; color: #444; }
    </style>
</head>
<body>
    <nav><a onclick="location.reload()">Inicio</a></nav>
    <div class="ad-slot">ANUNCIO ADSENSE</div>
    <div class="main-card">
        <h1>🚀 MOTOR PRO</h1>
        <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
        <div class="options">
            <select id="formatInput">
                <option value="mp4">🎬 Video MP4</option>
                <option value="mp3">🎵 Audio MP3</option>
            </select>
        </div>
        <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
        <div id="status" style="margin-top:20px;"></div>
        <div id="previewSection">
            <img id="videoThumbnail" src="">
            <div id="videoTitle" style="margin-bottom:15px; font-weight:bold;"></div>
            <a id="finalDownloadBtn" href="#">CONFIRMAR DESCARGA</a>
        </div>
    </div>
    <div class="ad-slot">ANUNCIO ADSENSE</div>
    <script>
        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            if(!url) return alert("Pega un link");
            s.innerText = "⏳ Obteniendo información...";
            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const info = await res.json();
                if(info.success) {
                    document.getElementById('videoThumbnail').src = info.thumbnail;
                    document.getElementById('videoTitle').innerText = info.title;
                    p.style.display = 'block';
                    s.innerText = "✅ Video encontrado";
                    document.getElementById('finalDownloadBtn').onclick = (e) => {
                        e.preventDefault();
                        generateDownload(url, document.getElementById('formatInput').value);
                    };
                } else { s.innerText = "❌ No se encontró info."; }
            } catch (e) { s.innerText = "❌ Error de conexión."; }
        }
        async function generateDownload(url, tipo) {
            const s = document.getElementById('status');
            s.innerText = "⏳ Generando link de descarga...";
            try {
                const res = await fetch(`/api/down?url=${encodeURIComponent(url)}&type=${tipo}`);
                const data = await res.json();
                if(data.url) {
                    s.innerText = "✅ ¡Listo! Descargando...";
                    window.location.href = data.url;
                } else { s.innerText = "❌ Error en el motor."; }
            } catch (e) { s.innerText = "❌ Error de descarga."; }
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
    try:
        r = requests.get("https://download-all-in-one-lite.p.rapidapi.com/autolink", 
                        params={"url": url}, 
                        headers={"x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585", "x-rapidapi-host": "download-all-in-one-lite.p.rapidapi.com"}, 
                        timeout=15)
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
