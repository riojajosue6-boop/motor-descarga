import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA (Solo para búsqueda)
def get_ydl_opts():
    return {
        'proxy': f"http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80",
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

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
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 22px; border-radius: 18px; text-decoration: none; font-weight: bold; margin-top: 25px; font-size: 18px; display: inline-block; width: 80%; box-shadow: 0 0 20px var(--success); }
    </style>
</head>
<body>
    <div class="card">
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:12px; font-weight:bold;">MODO DESCARGA DIRECTA ACTIVADO ⚡</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí...">
        <button id="mainBtn" onclick="procesar()">ARRANCAR MOTOR</button>
        <div id="result">
            <p id="status" style="margin-top:20px; color:#aaa;"></p>
            <a id="dlLink" class="dl-btn" href="#" download="video_motor_pro.mp4">📥 GUARDAR VIDEO</a>
        </div>
    </div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dlLink = document.getElementById('dlLink');
            const btn = document.getElementById('mainBtn');
            if(!url) return;
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerHTML = "📡 Buscando enlace en USA...";
            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = "✅ ¡Enlace capturado!<br>Haz clic abajo para descargar directamente.";
                    dlLink.href = data.url;
                    dlLink.style.display = 'block';
                    btn.disabled = false;
                } else {
                    status.innerText = "❌ No se pudo obtener el video.";
                    btn.disabled = false;
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión.";
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
            # Enviamos el link directo al navegador del usuario
            return jsonify({"success": True, "url": i.get('url')})
    except Exception as e:
        return jsonify({"success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
