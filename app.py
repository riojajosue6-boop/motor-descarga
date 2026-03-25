import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA (WEBSHARE)
# Solo lo usamos para extraer la información, no para la descarga pesada.
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

# INTERFAZ PREMIUM NEÓN (MOTOR PRO BOLIVIA)
HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀 | Cloud Direct</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 40px 20px; border-radius: 30px; border: 1px solid #333; max-width: 480px; margin: 40px auto; box-shadow: 0 20px 60px rgba(0,0,0,1); }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 35px; font-weight: 900; }
        .mode-badge { background: #222; color: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 10px; border: 1px solid var(--primary); display: inline-block; margin-bottom: 15px; }
        input { width: 100%; padding: 22px; border-radius: 18px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; outline: none; margin: 25px 0; font-size: 16px; }
        #mainBtn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: bold; cursor: pointer; text-transform: uppercase; font-size: 16px; transition: 0.3s; }
        #mainBtn:hover { transform: scale(1.02); background: var(--primary); }
        #mainBtn:disabled { opacity: 0.3; cursor: not-allowed; }
        .dl-btn { display: none; background: var(--success); color: #fff; padding: 22px; border-radius: 18px; text-decoration: none; font-weight: bold; margin-top: 25px; font-size: 18px; display: none; box-shadow: 0 0 25px var(--success); }
        .footer { margin-top: 50px; font-size: 11px; color: #444; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="mode-badge">DIRECT DOWNLOAD MODE ⚡</div>
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:12px; margin-top:5px; font-weight:bold;">BY JOSUE • COCHABAMBA</p>
        
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí..." autocomplete="off">
        <button id="mainBtn" onclick="procesar()">ARRANCAR MOTOR</button>
        
        <div id="result">
            <p id="status" style="margin-top:20px; color:#aaa; font-size:14px;"></p>
            <a id="dlLink" class="dl-btn" href="#" target="_blank">📥 GUARDAR VIDEO</a>
        </div>
    </div>
    <div class="footer">© 2026 MOTOR PRO BOLIVIA</div>

    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dlLink = document.getElementById('dlLink');
            const btn = document.getElementById('mainBtn');
            
            if(!url) return;
            btn.disabled = true;
            dlLink.style.display = 'none';
            status.innerHTML = "⏳ <span style='color:var(--primary)'>Buscando enlace seguro...</span>";

            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = "✅ ¡Enlace generado!<br><small>Haz clic abajo para descargar.</small>";
                    dlLink.href = data.url;
                    dlLink.style.display = 'block';
                    
                    // Truco para forzar descarga en algunos navegadores móviles
                    dlLink.setAttribute('download', 'video_motor_pro.mp4');
                    
                } else {
                    status.innerHTML = "❌ <span style='color:var(--secondary)'>Error al obtener el video.</span>";
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión con el servidor.";
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
    return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    # Limpiamos el link de parámetros innecesarios
    if "?" in u: u = u.split("?")[0]
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            # Retornamos el link directo para que el usuario descargue desde su IP
            return jsonify({"success": True, "url": i.get('url')})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False})

if __name__ == "__main__":
    # Railway asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
