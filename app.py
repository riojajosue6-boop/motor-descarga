import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES Y COOKIES ---
def get_ydl_opts():
    user = "ksvyuzxs-rotate"
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'format': 'best',
        # Cambiamos a cliente "WEB" que es más robusto con cookies
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'socket_timeout': 40,
        'extractor_args': {'youtube': {'player_client': ['web', 'android']}},
        'http_headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    # SI EL ARCHIVO EXISTE, LO USAMOS (Esto es lo que falta)
    if os.path.exists(cookie_path):
        opts['cookiefile'] = cookie_path
        print("✅ Usando archivo cookies.txt detectado.")
    else:
        print("⚠️ No se encontró cookies.txt, intentando sin cookies...")

    return opts

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Motor Pro 🚀 | Cochabamba</title>
        <style>
            body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 40px 20px; }
            .card { background: #111; padding: 35px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: auto; }
            h1 { color: #ff0000; font-size: 26px; }
            input { width: 100%; padding: 18px; border-radius: 12px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; font-size: 16px; margin-bottom: 20px; }
            button { width: 100%; padding: 18px; background: #ff0000; color: #fff; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; }
            #res { margin-top: 30px; font-weight: bold; min-height: 60px; }
            .dl-link { display: block; background: #00aa00; color: #fff; padding: 18px; border-radius: 12px; text-decoration: none; margin-top: 10px; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 MOTOR PRO</h1>
            <p style="font-size:11px; color:#555">Sistema con Cookies y Proxy Residencial Activo</p>
            <input type="text" id="url" placeholder="Pega el link aquí..." autocomplete="off">
            <button id="btn" onclick="descargar()">PROCESAR VIDEO</button>
            <div id="res"></div>
        </div>
        <script>
            async function descargar() {
                const u = document.getElementById('url').value;
                const r = document.getElementById('res');
                const b = document.getElementById('btn');
                if(!u) return;
                b.disabled = true; r.innerHTML = "⏳ Validando sesión con YouTube...";
                try {
                    const resp = await fetch('/api/info?url=' + encodeURIComponent(u));
                    const data = await resp.json();
                    if(data.success) {
                        r.innerHTML = '✅ LISTO!<br><a class="dl-link" href="' + data.url + '" target="_blank">DESCARGAR AHORA</a>';
                    } else { 
                        r.innerHTML = "❌ YouTube sigue bloqueando la IP.<br><small>Espera 5 segundos y dale a 'PROCESAR' de nuevo.</small>"; 
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
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
