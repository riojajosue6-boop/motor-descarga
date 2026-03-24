import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES (WEBSHARE BACKBONE) ---
def get_ydl_opts():
    # Datos exactos de tu captura de Webshare
    user = "ksvyuzxs"
    pw = "r148qqniiwdz"
    # Usamos la conexión Backbone por el puerto 80 como indica tu lista
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'socket_timeout': 30
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
            .card { background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; max-width: 400px; margin: auto; }
            input { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; }
            button { width: 100%; padding: 15px; background: #ff0000; color: #fff; border: none; border-radius: 10px; margin-top: 20px; font-weight: bold; cursor: pointer; }
            #res { margin-top: 25px; font-weight: bold; }
            a { display: block; background: #00aa00; color: #fff; padding: 15px; border-radius: 10px; text-decoration: none; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚀 MOTOR PRO</h2>
            <p style="font-size:12px; color:#666;">Optimizando conexión residencial...</p>
            <input type="text" id="url" placeholder="Pega el link aquí...">
            <button id="btn" onclick="descargar()">PROCESAR VIDEO</button>
            <div id="res"></div>
        </div>
        <script>
            async function descargar() {
                const u = document.getElementById('url').value;
                const r = document.getElementById('res');
                const b = document.getElementById('btn');
                if(!u) return alert("Pega un link");
                b.disabled = true; r.innerText = "⏳ Analizando (esto puede tardar 10s)...";
                try {
                    const resp = await fetch('/api/info?url=' + encodeURIComponent(u));
                    const data = await resp.json();
                    if(data.success) {
                        r.innerHTML = '✅ ¡ENCONTRADO!<br><a href="' + data.url + '">DESCARGAR AHORA</a>';
                    } else { r.innerText = "❌ Error: YouTube bloqueó este intento. Prueba con otro link o reintenta."; }
                } catch(e) { r.innerText = "❌ Error de conexión con el servidor."; }
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
        print(f"DEBUG: {e}")
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
