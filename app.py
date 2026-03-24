import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# WEBSHARE PROXY (Solo para búsqueda, no para descarga)
def get_ydl_opts():
    return {
        'proxy': f"http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80",
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

HTML_FINAL = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Directo</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #151515; padding: 40px; border-radius: 30px; border: 1px solid #333; max-width: 450px; margin: auto; box-shadow: 0 20px 50px #000; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; }
        input { width: 100%; padding: 20px; border-radius: 15px; border: 1px solid #333; background: #222; color: #fff; margin: 20px 0; box-sizing: border-box; }
        #btn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        #downloadBtn { display: none; background: #2ecc71; color: white; padding: 20px; border-radius: 15px; text-decoration: none; display: none; margin-top: 20px; font-weight: bold; box-shadow: 0 0 20px #2ecc71; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p style="font-size: 10px; color: #555;">TECNOLOGÍA DE DESCARGA DIRECTA</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok...">
        <button id="btn" onclick="obtener()">OBTENER VIDEO</button>
        <div id="status" style="margin-top: 20px; color: #888;"></div>
        <a id="downloadBtn" href="#" target="_blank">📥 GUARDAR EN DISPOSITIVO</a>
    </div>

    <script>
        async function obtener() {
            const url = document.getElementById('urlInput').value;
            const status = document.getElementById('status');
            const dl = document.getElementById('downloadBtn');
            const btn = document.getElementById('btn');
            
            btn.disabled = true;
            status.innerText = "⏳ Buscando en los servidores de TikTok...";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await res.json();
                
                if(data.success) {
                    status.innerHTML = "✅ ¡Enlace generado!<br>Mantén presionado el botón o haz clic para guardar.";
                    dl.href = data.url;
                    dl.style.display = "block";
                    // Forzamos descarga en algunos navegadores
                    dl.setAttribute('download', 'video_motor_pro.mp4');
                } else {
                    status.innerText = "❌ No se pudo extraer el video.";
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
def index(): return render_template_string(HTML_FINAL)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            info = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": info['url']})
    except: return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
