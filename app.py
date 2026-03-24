import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN MAESTRA DE PROXIES
# Usamos -rotate para que Webshare nos de una IP nueva cada vez
def get_ydl_opts():
    user = "ksvyuzxs-rotate"
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        # Engañamos a YT pareciendo un iPhone 15
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
        'socket_timeout': 60,
        'extract_flat': False,
    }

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Motor Pro 🇧🇴</title>
        <style>
            body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 40px 20px; }
            .card { background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; max-width: 400px; margin: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
            input { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; font-size: 16px; }
            button { width: 100%; padding: 15px; background: #ff0000; color: #fff; border: none; border-radius: 10px; margin-top: 20px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            button:active { transform: scale(0.95); }
            #res { margin-top: 25px; font-weight: bold; min-height: 50px; }
            .dl-btn { display: block; background: #00aa00; color: #fff; padding: 15px; border-radius: 10px; text-decoration: none; margin-top: 10px; animation: pulse 2s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="card">
            <h2 style="color:#ff0000">🚀 MOTOR PRO</h2>
            <p style="font-size:11px; color:#555;">Conexión Residencial Rotativa Activa</p>
            <input type="text" id="url" placeholder="Pega el link de YouTube Shorts...">
            <button id="btn" onclick="descargar()">PROCESAR VIDEO</button>
            <div id="res"></div>
        </div>
        <script>
            async function descargar() {
                const u = document.getElementById('url').value;
                const r = document.getElementById('res');
                const b = document.getElementById('btn');
                if(!u) return alert("Pega un link");
                b.disabled = true; r.innerHTML = "⏳ Saltando bloqueos de YouTube...<br><small>Esto toma unos segundos</small>";
                try {
                    const resp = await fetch('/api/info?url=' + encodeURIComponent(u));
                    const data = await resp.json();
                    if(data.success) {
                        r.innerHTML = '✅ ¡VÍDEO LISTO!<br><a class="dl-btn" href="' + data.url + '" target="_blank">DESCARGAR AHORA</a>';
                    } else { 
                        r.innerHTML = "❌ YouTube bloqueó la IP. <br><button onclick='descargar()' style='background:#333; font-size:10px; width:auto; padding:5px 10px;'>REINTENTAR NUEVA IP</button>"; 
                    }
                } catch(e) { r.innerText = "❌ Error de servidor."; }
                b.disabled = false;
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url'), "title": i.get('title')})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
