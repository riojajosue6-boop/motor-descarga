import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA (WEB SHARE)
def get_ydl_opts():
    user = "ksvyuzxs-us-rotate"
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

# INTERFAZ PULIDA CON ESTÉTICA NEÓN
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Cochabamba</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 35px; border-radius: 25px; border: 1px solid #333; max-width: 480px; margin: 50px auto; box-shadow: 0 15px 50px rgba(0,0,0,0.9); }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 32px; font-weight: 800; }
        input { width: 100%; padding: 20px; border-radius: 15px; border: 1px solid #333; background: #222; color: #fff; box-sizing: border-box; outline: none; margin: 25px 0; font-size: 16px; }
        input:focus { border-color: var(--primary); }
        #mainBtn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        #mainBtn:hover { background: var(--primary); transform: scale(1.02); }
        #mainBtn:disabled { opacity: 0.5; cursor: not-allowed; }
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 20px; border-radius: 15px; text-decoration: none; font-weight: bold; margin-top: 25px; box-shadow: 0 0 25px var(--success); font-size: 18px; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
        .footer { margin-top: 60px; font-size: 12px; color: #444; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p style="color:#666; font-size:12px; margin-top:10px; font-weight:bold;">USA PROXY CLOUD ACTIVATED</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí..." spellcheck="false">
        <button id="mainBtn" onclick="procesar()">INICIAR PROCESO</button>
        <div id="result">
            <p id="status" style="margin-top:25px; color:#aaa; font-size:14px;"></p>
            <a id="dlLink" class="dl-btn" href="#">📥 DESCARGAR VIDEO AHORA</a>
        </div>
    </div>
    <div class="footer">© 2026 MOTOR PRO BOLIVIA • BY JOSUE</div>
    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dlLink = document.getElementById('dlLink');
            const btn = document.getElementById('mainBtn');
            if(!url) return;
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerHTML = "📡 Conectando con servidor residencial USA...";
            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = "✅ Enlace validado. <br>Haga clic abajo para descargar.";
                    dlLink.href = "/descargar_archivo?url=" + encodeURIComponent(data.url);
                    dlLink.style.display = 'block';
                    btn.disabled = false;
                } else {
                    status.innerHTML = "❌ Error: Link inválido o protegido.";
                    btn.disabled = false;
                }
            } catch(e) {
                status.innerHTML = "❌ Error de conexión con Railway.";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    # Limpiamos el link de rastreadores
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
    if not video_url: return "URL ausente"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/',
        'Accept': '*/*'
    }
    
    try:
        # Usamos stream_with_context para manejar archivos grandes sin bloquear el servidor
        def generate():
            with requests.get(video_url, stream=True, headers=headers, timeout=60) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        yield chunk

        return Response(stream_with_context(generate()), 
                        content_type="video/mp4",
                        headers={"Content-Disposition": "attachment; filename=video_motorpro.mp4"})
    except Exception as e:
        return f"Error en puente: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, threaded=True) # Activamos hilos para mayor potencia
