import os
import yt_dlp
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES USA (WEBSHARE) ---
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

# --- INTERFAZ PREMIUM NEÓN (MOTOR PRO) ---
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Eléctrico</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; overflow-x: hidden; }
        .card { background: #151515; padding: 40px 20px; border-radius: 30px; border: 1px solid #333; max-width: 480px; margin: 40px auto; box-shadow: 0 20px 60px rgba(0,0,0,1); position: relative; }
        .card::before { content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px; background: linear-gradient(45deg, var(--primary), var(--secondary)); border-radius: 32px; z-index: -1; opacity: 0.3; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 35px; font-weight: 900; letter-spacing: -1px; }
        .badge { background: #222; color: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 10px; font-weight: bold; border: 1px solid var(--primary); display: inline-block; margin-bottom: 15px; }
        input { width: 100%; padding: 22px; border-radius: 18px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; outline: none; margin: 25px 0; font-size: 16px; transition: 0.3s; }
        input:focus { border-color: var(--primary); box-shadow: 0 0 15px rgba(0, 242, 234, 0.2); }
        #mainBtn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: 800; cursor: pointer; font-size: 16px; transition: 0.3s; text-transform: uppercase; }
        #mainBtn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }
        #mainBtn:disabled { opacity: 0.3; cursor: not-allowed; transform: none; }
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 22px; border-radius: 18px; text-decoration: none; font-weight: 800; margin-top: 25px; font-size: 18px; animation: glow 2s infinite; }
        @keyframes glow { 0% { box-shadow: 0 0 5px var(--success); } 50% { box-shadow: 0 0 30px var(--success); } 100% { box-shadow: 0 0 5px var(--success); } }
        .footer { margin-top: 50px; font-size: 11px; color: #444; text-transform: uppercase; letter-spacing: 2px; }
        #status { margin-top: 20px; font-size: 14px; color: #888; min-height: 40px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="badge">SERVER PRO • USA PROXY</div>
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:12px; margin-top:5px;">INSTANT DOWNLOADER</p>
        
        <input type="text" id="urlInput" placeholder="Pega el enlace de TikTok aquí..." autocomplete="off">
        <button id="mainBtn" onclick="procesar()">ARRANCAR MOTOR</button>
        
        <div id="result">
            <div id="status"></div>
            <a id="dlLink" class="dl-btn" href="#">⬇️ DESCARGAR AHORA</a>
        </div>
    </div>
    <div class="footer">© 2026 MOTOR PRO BOLIVIA • JOSUE</div>

    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dlLink = document.getElementById('dlLink');
            const btn = document.getElementById('mainBtn');
            
            if(!url) return;
            
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerHTML = "⏳ <span style='color:var(--primary)'>INYECTANDO PROXY USA...</span>";

            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = "✅ <span style='color:lime'>VIDEO CAPTURADO CON ÉXITO</span>";
                    setTimeout(() => {
                        dlLink.href = "/descargar_archivo?url=" + encodeURIComponent(data.url);
                        dlLink.style.display = 'block';
                        btn.disabled = false;
                    }, 500);
                } else {
                    status.innerHTML = "❌ <span style='color:var(--secondary)'>ERROR: EL VIDEO ESTÁ PROTEGIDO O EL LINK ES INVÁLIDO</span>";
                    btn.disabled = false;
                }
            } catch(e) {
                status.innerHTML = "❌ <span style='color:var(--secondary)'>ERROR DE COMUNICACIÓN CON EL SERVIDOR</span>";
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
    if "?" in u: u = u.split("?")[0]
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url')})
    except Exception as e:
        print(f"DEBUG INFO: {e}")
        return jsonify({"success": False})

@app.route('/descargar_archivo')
def descargar_archivo():
    video_url = request.args.get('url')
    if not video_url: return "URL ERROR"
    
    # DISFRAZ DE ALTO NIVEL PARA LA DESCARGA FINAL
    # Usamos Range: bytes=0- para que TikTok crea que es un streaming de video
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.tiktok.com/',
        'Range': 'bytes=0-',
        'Accept': '*/*'
    }
    
    try:
        # Iniciamos la descarga en modo Stream
        r = requests.get(video_url, headers=headers, stream=True, timeout=45)
        r.raise_for_status()
        
        def generate():
            # Chunks de 1MB para aprovechar la RAM de tu plan de pago
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    yield chunk

        # Entregamos la respuesta con el tamaño exacto del video (Content-Length)
        # Esto evita que Railway cierre la conexión por "falta de respuesta"
        response_headers = {
            "Content-Disposition": "attachment; filename=motor_pro_video.mp4",
            "Content-Type": "video/mp4"
        }
        if r.headers.get('Content-Length'):
            response_headers["Content-Length"] = r.headers.get('Content-Length')

        return Response(stream_with_context(generate()), headers=response_headers)
        
    except Exception as e:
        print(f"DEBUG DOWNLOAD ERROR: {e}")
        return f"Error en el puente de descarga: {str(e)}"

if __name__ == "__main__":
    # Railway inyecta el puerto automáticamente
    port = int(os.environ.get("PORT", 8080))
    # threaded=True permite que tu servidor de pago maneje múltiples descargas a la vez
    app.run(host="0.0.0.0", port=port, threaded=True)
