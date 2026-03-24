import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN DE PROXIES (WEBSHARE) ---
proxy_users = ["ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", "ksvyuzxs-9", "ksvyuzxs-10"]
proxy_pass = "r148qqniiwdz"
proxy_host = "p.webshare.io"
proxy_port = "80"

def get_proxy(index=0):
    user = proxy_users[index % len(proxy_users)]
    p_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    return {"http": p_url, "https": p_url}

# --- DISEÑO PREMIUM LIMPIO ---
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
        nav { background: #000; padding: 15px; border-bottom: 1px solid #333; margin-bottom: 20px; }
        nav a { color: #888; margin: 0 15px; text-decoration: none; font-size: 14px; cursor: pointer; }
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }
        h1 { color: var(--red); font-size: 28px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
        select { width: 100%; padding: 15px; margin: 15px 0; border-radius: 10px; background: #222; color: white; border: 1px solid #444; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 18px; cursor: pointer; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #supportBox { background: #1a2a1a; color: #99ff99; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #finalDownloadBtn { width: 100%; padding: 18px; background: #00aa00; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }
        #finalDownloadBtn:disabled { background: #333; opacity: 0.6; cursor: not-allowed; }
        footer { padding: 40px; color: #444; font-size: 12px; }
    </style>
</head>
<body>
    <nav>
        <a onclick="location.reload()">Inicio</a>
        <a>Privacidad</a>
        <a>Términos</a>
    </nav>
    <div class="container">
        <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8532381032470048" data-ad-slot="5199614767" data-ad-format="auto"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>

        <div class="main-card">
            <h1>🚀 MOTOR DE DESCARGA</h1>
            <p style="color:#666; font-size:12px;">YT • FB • IG • TT</p>
            <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
            <select id="formatInput">
                <option value="mp4">🎬 Video MP4</option>
                <option value="mp3">🎵 Audio MP3 (YouTube)</option>
            </select>
            <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
            <div id="status" style="margin-top:20px; font-weight:bold;"></div>

            <div id="previewSection">
                <img id="videoThumbnail" src="">
                <div id="videoTitle" style="margin:15px 0; font-weight:bold; color:#fff;"></div>
                <div id="supportBox">
                    ❤️ <strong>Apóyanos visitando las publicidades</strong> para mantener el servicio gratuito en Bolivia.
                    <span id="countdownText" style="display:block; margin-top:10px;">Activando botón en 5...</span>
                </div>
                <button id="finalDownloadBtn" disabled>DESCARGAR AHORA</button>
            </div>
        </div>
    </div>
    <footer>© 2026 Motor de Descarga Pro - Cochabamba 🇧🇴</footer>

    <script>
        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const fmt = document.getElementById('formatInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            if(!url) return alert("Pega un link");
            b.disabled = true; p.style.display = 'none'; s.innerText = "⏳ Analizando enlace...";
            try {
                const res = await fetch(`/api/info?url=${encodeURIComponent(url)}&type=${fmt}`);
                const data = await res.json();
                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; s.innerText = "✅ ¡Detectado!";
                    let timeLeft = 5;
                    const dBtn = document.getElementById('finalDownloadBtn');
                    dBtn.disabled = true;
                    const timer = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `Activando botón en ${timeLeft}...`;
                        if(timeLeft <= 0) { clearInterval(timer); document.getElementById('countdownText').style.display = 'none'; dBtn.disabled = false; }
                    }, 1000);
                    dBtn.onclick = () => { window.location.href = data.download_url; };
                } else { s.innerText = "❌ Error: Link no soportado."; }
            } catch (e) { s.innerText = "❌ Error de conexión."; }
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
    fmt = request.args.get('type', 'mp4')
    if not url: return jsonify({"success": False})
    for i in range(3):
        proxy = get_proxy(i)
        ydl_opts = {
            'proxy': proxy, 'quiet': True,
            'format': 'bestaudio/best' if fmt == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return jsonify({"success": True, "title": info.get('title'), "thumbnail": info.get('thumbnail'), "download_url": info.get('url')})
        except: continue
    return jsonify({"success": False})

@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
