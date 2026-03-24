import os
import yt_dlp
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
    return f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"

# --- DISEÑO PREMIUM ORIGINAL (CON CORRECCIÓN DE BOTÓN) ---
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
        .container { padding: 20px; max-width: 800px; margin: 0 auto; }
        .main-card { background: var(--gray); padding: 40px; border-radius: 25px; border: 1px solid #333; margin: 10px auto; }
        h1 { color: var(--red); font-size: 32px; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; box-sizing: border-box; }
        #btnAction { width: 100%; padding: 18px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; margin-top: 15px; cursor: pointer; }
        #previewSection { display: none; margin-top: 30px; border-top: 1px solid #333; padding-top: 20px; }
        #videoThumbnail { width: 100%; max-width: 400px; border-radius: 15px; border: 1px solid #444; }
        #supportBox { background: #1a2a1a; color: #99ff99; padding: 20px; border-radius: 15px; margin: 20px 0; font-size: 14px; }
        #finalDownloadBtn { width: 100%; padding: 18px; background: #00aa00; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }
        #finalDownloadBtn:disabled { background: #333; opacity: 0.6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card">
            <h1>🚀 MOTOR DE DESCARGA</h1>
            <input type="text" id="urlInput" placeholder="Pega el enlace aquí...">
            <select id="formatInput" style="width:100%; padding:15px; margin-top:10px; border-radius:10px; background:#222; color:white;">
                <option value="mp4">🎬 Video MP4</option>
                <option value="mp3">🎵 Audio MP3</option>
            </select>
            <button id="btnAction" onclick="processVideo()">PROCESAR VIDEO</button>
            <div id="status" style="margin-top:20px; font-weight:bold;"></div>
            <div id="previewSection">
                <img id="videoThumbnail" src="">
                <div id="videoTitle" style="margin:15px 0; font-weight:bold; color:#fff;"></div>
                <div id="supportBox">
                    ❤️ <strong>Apóyanos visitando las publicidades</strong> para mantener el servicio gratuito.
                    <span id="countdownText" style="display:block; margin-top:10px;">Activando en 5...</span>
                </div>
                <button id="finalDownloadBtn" disabled>CONFIRMAR DESCARGA</button>
            </div>
        </div>
    </div>
    <script>
        async function processVideo() {
            const url = document.getElementById('urlInput').value;
            const fmt = document.getElementById('formatInput').value;
            const s = document.getElementById('status');
            const p = document.getElementById('previewSection');
            const b = document.getElementById('btnAction');
            if(!url) return alert("Pega un link");
            b.disabled = true; p.style.display = 'none'; s.innerText = "⏳ Analizando...";
            try {
                const res = await fetch(`/api/extract?url=${encodeURIComponent(url)}&type=${fmt}`);
                const data = await res.json();
                if(data.success) {
                    document.getElementById('videoThumbnail').src = data.thumbnail;
                    document.getElementById('videoTitle').innerText = data.title;
                    p.style.display = 'block'; s.innerText = "✅ ¡Listo!";
                    let timeLeft = 5;
                    const dBtn = document.getElementById('finalDownloadBtn');
                    dBtn.disabled = true;
                    const timer = setInterval(() => {
                        timeLeft--;
                        document.getElementById('countdownText').innerText = `Activando en ${timeLeft}...`;
                        if(timeLeft <= 0) { 
                            clearInterval(timer); 
                            document.getElementById('countdownText').style.display = 'none'; 
                            dBtn.disabled = false; 
                        }
                    }, 1000);
                    // SOLUCIÓN AL "UNDEFINED": Usamos directamente la URL que envía el servidor
                    dBtn.onclick = () => { window.location.href = data.download_url; };
                } else { s.innerText = "❌ Error al procesar."; }
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
def extract():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    if not url: return jsonify({"success": False})

    for i in range(3):
        proxy = get_proxy(i)
        ydl_opts = {
            'proxy': proxy,
            'quiet': True,
            'format': 'bestaudio/best' if fmt == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return jsonify({
                    "success": True,
                    "title": info.get('title', 'Video'),
                    "thumbnail": info.get('thumbnail', ''),
                    "download_url": info.get('url') # Pasamos el link directo para que el cel no se bloquee
                })
        except: continue
    return jsonify({"success": False})

@app.route('/ads.txt')
def ads_txt():
    return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
