    app.run(host="0.0.0.0", port=port)
import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# --- CONFIGURACIÓN DE PROXIES (WEBSHARE) ---
P_USER = os.environ.get("PROXY_USER", "ksvyuzxs")
P_PASS = os.environ.get("PROXY_PASS", "r148qqniiwdz")
PROXY_URL = f"http://{P_USER}:{P_PASS}@p.webshare.io:80"

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Motor de Descarga Pro</title>
    <style>
        body { background: #0a0a0a; color: #eee; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #1a1a1a; padding: 30px; border-radius: 20px; border: 1px solid #333; max-width: 400px; margin: auto; }
        input { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #ff0000; color: white; border: none; border-radius: 10px; font-weight: bold; margin-top: 15px; cursor: pointer; }
        #status { margin-top: 20px; font-weight: bold; }
        #preview { display: none; margin-top: 20px; border-top: 1px solid #333; padding-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <input type="text" id="url" placeholder="Pega el enlace aquí...">
        <button id="btn" onclick="process()">PROCESAR VIDEO</button>
        <div id="status"></div>
        <div id="preview">
            <p id="vTitle"></p>
            <button style="background: #00aa00;" id="dl">DESCARGAR AHORA</button>
        </div>
    </div>
    <script>
        async function process() {
            const url = document.getElementById('url').value;
            const s = document.getElementById('status');
            const p = document.getElementById('preview');
            const b = document.getElementById('btn');
            if(!url) return alert("Pega un link");
            b.disabled = true; s.innerText = "⏳ Analizando...";
            try {
                const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
                const data = await res.json();
                if(data.success) {
                    document.getElementById('vTitle').innerText = data.title;
                    p.style.display = 'block'; s.innerText = "✅ ¡Listo!";
                    document.getElementById('dl').onclick = () => window.location.href = data.download_url;
                } else { s.innerText = "❌ Error: Reintenta en 10 seg."; }
            } catch(e) { s.innerText = "❌ Error de conexión."; }
            b.disabled = false;
        }
    </script>
</body>
</html>
""")

@app.route('/api/info')
def api_info():
    url = request.args.get('url')
    if not url: return jsonify({"success": False})
    ydl_opts = {
        'proxy': PROXY_URL,
        'quiet': True,
        'format': 'best',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"success": True, "title": info.get('title'), "download_url": info.get('url')})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
