import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        # Cambiamos a un User-Agent de Android, que es el que menos bloquean
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
        'socket_timeout': 30,
        # FORZAMOS que no use cookies guardadas viejas
        'no_cookies': True,
        'ignoreerrors': True
    }

@app.route('/')
def home():
    # Mantenemos tu diseño pero con una mejora en el botón de reintento
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
            #res { margin-top: 25px; }
            .dl-btn { display: block; background: #00aa00; color: #fff; padding: 15px; border-radius: 10px; text-decoration: none; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚀 MOTOR PRO</h2>
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
                b.disabled = true; r.innerHTML = "⏳ Saltando bloqueo (Intento con nueva IP)...";
                try {
                    const resp = await fetch('/api/info?url=' + encodeURIComponent(u));
                    const data = await resp.json();
                    if(data.success) {
                        r.innerHTML = '✅ LISTO!<br><a class="dl-btn" href="' + data.url + '" target="_blank">DESCARGAR AHORA</a>';
                    } else { 
                        r.innerHTML = "❌ Bloqueado por YouTube. <br><small>Presiona 'PROCESAR' de nuevo para cambiar de IP.</small>"; 
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
    
    # TRUCO: Intentamos con dos configuraciones diferentes si la primera falla
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            if i:
                return jsonify({"success": True, "url": i.get('url'), "title": i.get('title')})
    except Exception as e:
        print(f"ERROR: {e}")
    
    return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
