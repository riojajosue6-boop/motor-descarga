import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA
def get_ydl_opts():
    return {
        'proxy': f"http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80",
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

# INTERFAZ PREMIUM NEÓN
HTML_MASTER = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 40px 20px; border-radius: 30px; border: 1px solid #333; max-width: 480px; margin: 40px auto; box-shadow: 0 20px 60px rgba(0,0,0,1); }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 35px; font-weight: 900; }
        input { width: 100%; padding: 22px; border-radius: 18px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; outline: none; margin: 25px 0; font-size: 16px; }
        #mainBtn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        #mainBtn:disabled { opacity: 0.3; }
        .progress-container { margin: 20px 0; background: #222; border-radius: 10px; height: 10px; display: none; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: var(--primary); transition: 1s linear; }
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 22px; border-radius: 18px; text-decoration: none; font-weight: bold; margin-top: 25px; font-size: 18px; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:12px; font-weight:bold;">PREMIUM CLOUD • BOLIVIA 🇧🇴</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí...">
        <button id="mainBtn" onclick="procesar()">INICIAR PROCESO</button>
        <div id="result">
            <p id="status" style="margin-top:20px; color:#aaa;"></p>
            <div class="progress-container" id="pContainer"><div class="progress-bar" id="pBar"></div></div>
            <a id="dlLink" class="dl-btn" href="#">⬇️ DESCARGAR AHORA</a>
        </div>
    </div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dlLink = document.getElementById('dlLink');
            const btn = document.getElementById('mainBtn');
            const pBar = document.getElementById('pBar');
            const pContainer = document.getElementById('pContainer');
            if(!url) return;
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerHTML = "📡 Conectando con servidor USA...";
            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = "✅ ¡Video listo! Preparando descarga segura...";
                    pContainer.style.display = 'block';
                    let seg = 8;
                    const timer = setInterval(() => {
                        seg--;
                        pBar.style.width = ((8-seg)/8)*100 + "%";
                        if(seg <= 0) {
                            clearInterval(timer);
                            pContainer.style.display = 'none';
                            status.innerHTML = "<span style='color:lime'>¡LISTO PARA BAJAR!</span>";
                            dlLink.href = "/descargar_archivo?url=" + encodeURIComponent(data.url);
                            dlLink.style.display = 'block';
                            btn.disabled = false;
                        }
                    }, 1000);
                } else {
                    status.innerText = "❌ No se pudo obtener el video.";
                    btn.disabled = false;
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión con Railway.";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_MASTER)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    if "?" in u: u = u.split("?")[0]
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url')})
    except Exception as e:
        print(f"Log Error: {e}")
        return jsonify({"success": False})

@app.route('/descargar_archivo')
def descargar_archivo():
    video_url = request.args.get('url')
    if not video_url: return "URL Error"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/',
        'Range': 'bytes=0-'
    }
    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=60)
        r.raise_for_status()
        def generate():
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk: yield chunk
        response_headers = {
            "Content-Disposition": "attachment; filename=motor_pro_video.mp4",
            "Content-Type": "video/mp4"
        }
        if r.headers.get('Content-Length'):
            response_headers["Content-Length"] = r.headers.get('Content-Length')
        return Response(stream_with_context(generate()), headers=response_headers)
    except Exception as e:
        return f"Error en puente: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=True)
