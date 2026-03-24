import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES (WEBSHARE ROTATIVO) ---
def get_ydl_opts():
    # Usamos el usuario con -rotate para que Webshare cambie la IP en cada clic
    user = "ksvyuzxs-rotate"
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        # Engañamos a YouTube pareciendo un celular Android moderno
        'user_agent': 'Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'socket_timeout': 30,
        'no_cookies': True
    }

# --- DISEÑO DE LA PÁGINA (HTML + CSS + JS) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Cochabamba 🇧🇴</title>
    <style>
        :root { --red: #ff0000; --dark: #0a0a0a; --gray: #1a1a1a; --text: #eee; }
        body { background: var(--dark); color: var(--text); font-family: 'Segoe UI', sans-serif; margin: 0; padding: 40px 20px; text-align: center; }
        .card { background: var(--gray); padding: 35px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: auto; box-shadow: 0 15px 50px rgba(0,0,0,0.7); }
        h1 { color: var(--red); font-size: 26px; margin-bottom: 5px; }
        p.sub { font-size: 11px; color: #666; margin-bottom: 25px; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; }
        input:focus { border-color: var(--red); }
        button { width: 100%; padding: 18px; background: var(--red); color: #fff; border: none; border-radius: 12px; margin-top: 20px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #cc0000; transform: scale(1.02); }
        button:disabled { background: #444; cursor: not-allowed; }
        #result { margin-top: 30px; min-height: 60px; font-weight: bold; }
        .dl-link { display: block; background: #00aa00; color: #fff; padding: 18px; border-radius: 12px; text-decoration: none; margin-top: 10px; font-size: 18px; box-shadow: 0 5px 15px rgba(0,170,0,0.3); }
        footer { margin-top: 40px; font-size: 12px; color: #444; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p class="sub">Youtube • Facebook • Instagram • TikTok</p>
        
        <input type="text" id="videoUrl" placeholder="Pega el enlace aquí..." autocomplete="off">
        
        <button id="mainBtn" onclick="procesarVideo()">PROCESAR VIDEO</button>
        
        <div id="result"></div>
    </div>

    <footer>© 2026 Motor de Descarga Pro - Cochabamba 🇧🇴</footer>

    <script>
        async function procesarVideo() {
            const urlInput = document.getElementById('videoUrl');
            const resDiv = document.getElementById('result');
            const btn = document.getElementById('mainBtn');
            const url = urlInput.value.trim();

            if (!url || url.includes('import os')) {
                alert("Por favor, pega un enlace válido de video.");
                return;
            }

            btn.disabled = true;
            resDiv.innerHTML = "⏳ Saltando bloqueos de seguridad...<br><small style='color:#888'>Cambiando IP residencial...</small>";

            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();

                if (data.success) {
                    resDiv.innerHTML = `
                        <span style="color:lime">✅ ¡VÍDEO DETECTADO!</span><br>
                        <small style="color:#aaa">${data.title.substring(0, 40)}...</small>
                        <a href="${data.url}" class="dl-link" target="_blank">DESCARGAR AHORA</a>
                    `;
                } else {
                    resDiv.innerHTML = `
                        <span style="color:red">❌ YouTube bloqueó la IP actual.</span><br>
                        <button onclick="procesarVideo()" style="background:#333; padding:8px; font-size:12px; width:auto">REINTENTAR NUEVA IP</button>
                    `;
                }
            } catch (error) {
                resDiv.innerHTML = "<span style='color:red'>❌ Error de conexión con el servidor.</span>";
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/info')
def info():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "No URL provided"})
    
    try:
        # Intentamos extraer la información usando yt-dlp con los proxies residenciales
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            info_data = ydl.extract_info(video_url, download=False)
            if info_data:
                return jsonify({
                    "success": True,
                    "url": info_data.get('url'),
                    "title": info_data.get('title', 'Video detectado')
                })
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
    
    return jsonify({"success": False})

if __name__ == "__main__":
    # Railway asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
