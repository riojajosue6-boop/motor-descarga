import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

HTML_PRO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 30px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: 40px auto; box-shadow: 0 10px 40px rgba(0,0,0,0.8); }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 30px; margin: 0; }
        input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #333; background: #222; color: #fff; box-sizing: border-box; margin: 20px 0; outline: none; }
        #mainBtn { width: 100%; padding: 18px; background: #fff; color: #000; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }
        .dl-btn { display: none; background: #2ecc71; color: #fff; padding: 18px; border-radius: 12px; text-decoration: none; font-weight: bold; margin-top: 20px; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 MOTOR PRO</h1>
        <p style="color:#666; font-size:12px;">DESCARGA DIRECTA (SIN BLOQUEOS)</p>
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí...">
        <button id="mainBtn" onclick="procesar()">GENERAR DESCARGA</button>
        <div id="status" style="margin-top:20px; color:#aaa;"></div>
        <button id="forceDl" class="dl-btn">📥 CLIC PARA GUARDAR VIDEO</button>
    </div>

    <script>
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const btn = document.getElementById('mainBtn');
            const dlBtn = document.getElementById('forceDl');
            
            if(!url) return;
            btn.disabled = true;
            status.innerText = "⏳ Extrayendo link seguro...";

            try {
                const response = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = "✅ ¡Video listo!";
                    dlBtn.style.display = 'block';
                    // LA CLAVE: El navegador del usuario descarga, NO el servidor
                    dlBtn.onclick = () => {
                        const a = document.createElement('a');
                        a.href = data.url;
                        a.download = 'video_motor_pro.mp4';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    };
                } else {
                    status.innerText = "❌ Error al obtener el video.";
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
def home(): return render_template_string(HTML_PRO)

@app.route('/api/info')
def info():
    u = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            # Enviamos el link directo de los servidores de TikTok al usuario
            return jsonify({"success": True, "url": i.get('url')})
    except:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
