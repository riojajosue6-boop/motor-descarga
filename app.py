import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA (WEBSHARE)
def get_ydl_opts():
    proxy = "http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80"
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

HTML_PWA = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀</title>
    <link rel="manifest" href="/manifest.json">
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; padding: 20px; text-align: center; }
        .card { background: #151515; padding: 40px 20px; border-radius: 30px; border: 1px solid #333; max-width: 450px; margin: auto; box-shadow: 0 20px 50px #000; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; font-weight: 900; }
        input { width: 100%; padding: 20px; border-radius: 15px; border: 1px solid #333; background: #222; color: #fff; margin: 25px 0; box-sizing: border-box; outline: none; }
        #btn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        .dl-btn { display: none; background: #2ecc71; color: white; padding: 22px; border-radius: 18px; text-decoration: none; margin-top: 25px; font-weight: bold; display: none; box-shadow: 0 0 20px #2ecc71; }
    </style>
</head>
<body>
    <div class="card">
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:11px; font-weight:bold;">MODO TÚNEL USA ACTIVO 🛰️</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí...">
        <button id="btn" onclick="procesar()">INICIAR DESCARGA</button>
        <div id="status" style="margin-top:20px; color:#aaa;"></div>
        <a id="dlLink" class="dl-btn" href="#">📥 GUARDAR EN GALERÍA</a>
    </div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dl = document.getElementById('dlLink');
            const btn = document.getElementById('btn');
            if(!url) return;
            btn.disabled = true;
            dl.style.display = "none";
            status.innerHTML = "⏳ <span style='color:var(--primary)'>Extrayendo video mediante USA...</span>";
            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await res.json();
                if(data.success) {
                    status.innerHTML = "✅ ¡Video listo! <br>Haz clic para descargar.";
                    dl.href = "/tunel?url=" + encodeURIComponent(data.url);
                    dl.style.display = "block";
                } else {
                    status.innerText = "❌ No se pudo capturar el video.";
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión.";
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_PWA)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i['url']})
    except: return jsonify({"success": False})

@app.route('/tunel')
def tunel():
    video_url = request.args.get('url')
    # USAMOS EL PROXY TAMBIÉN PARA LA DESCARGA
    proxy = {"http": "http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80", "https": "http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80"}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Referer': 'https://www.tiktok.com/'}
    
    try:
        def generate():
            with requests.get(video_url, stream=True, headers=headers, proxies=proxy, timeout=60) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024*1024):
                    yield chunk
        
        return Response(stream_with_context(generate()), content_type="video/mp4", headers={"Content-Disposition": "attachment; filename=video_motorpro.mp4"})
    except Exception as e:
        return str(e)

@app.route('/manifest.json')
def manifest():
    return jsonify({"name": "Motor Pro", "short_name": "MotorPro", "start_url": "/", "display": "standalone", "background_color": "#0a0a0a", "theme_color": "#00f2ea", "icons": [{"src": "https://cdn-icons-png.flaticon.com/512/2583/2583130.png", "sizes": "512x512", "type": "image/png"}]})

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('fetch', function(event) {});", mimetype='application/javascript')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
