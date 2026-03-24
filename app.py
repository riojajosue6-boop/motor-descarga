import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de Proxies
def get_proxy():
    user = os.environ.get("PROXY_USER", "ksvyuzxs")
    pw = os.environ.get("PROXY_PASS", "r148qqniiwdz")
    url = f"http://{user}:{pw}@p.webshare.io:80"
    return {"http": url, "https": url}

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Motor Pro</title>
        <style>
            body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 50px 20px; }
            .box { background: #111; padding: 30px; border-radius: 15px; border: 1px solid #333; max-width: 400px; margin: auto; }
            input { width: 100%; padding: 15px; border-radius: 8px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; }
            button { width: 100%; padding: 15px; background: red; color: #fff; border: none; border-radius: 8px; margin-top: 20px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🚀 MOTOR DE DESCARGA</h2>
            <input type="text" id="url" placeholder="Pega el link aquí...">
            <button onclick="descargar()">PROCESAR</button>
            <p id="msg"></p>
        </div>
        <script>
            async function descargar() {
                const u = document.getElementById('url').value;
                const m = document.getElementById('msg');
                if(!u) return alert("Pega un link");
                m.innerText = "⏳ Procesando...";
                try {
                    const r = await fetch('/api/info?url=' + encodeURIComponent(u));
                    const d = await r.json();
                    if(d.success) {
                        m.innerHTML = '<a href="' + d.url + '" style="color:lime; font-weight:bold; text-decoration:none;">✅ CLIC PARA DESCARGAR</a>';
                    } else { m.innerText = "❌ Error en el link"; }
                } catch(e) { m.innerText = "❌ Error de servidor"; }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/info')
def info():
    u = request.args.get('url')
    opts = {
        'proxy': get_proxy()['http'],
        'quiet': True,
        'format': 'best',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            i = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": i.get('url')})
    except:
        return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
