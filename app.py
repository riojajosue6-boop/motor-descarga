import os
import requests
import re
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"

user_registry = {}

def get_clean_url(raw_url):
    url_match = re.search(r'(https?://[^\s\'"<>]+)', raw_url)
    return url_match.group(1) if url_match else None

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TurboLink Pro</title>
        <style>
            :root { --cian: #00f2ea; --bg: #050505; }
            body { background: var(--bg); color: #fff; font-family: sans-serif; text-align: center; padding: 20px; }
            .card { max-width: 450px; margin: auto; background: #121212; padding: 25px; border-radius: 20px; border: 1px solid #333; }
            input { width: 100%; padding: 15px; border-radius: 10px; border: 1px solid #444; background: #000; color: #fff; box-sizing: border-box; }
            .btn { width: 100%; padding: 15px; margin-top: 15px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; }
            .btn-main { background: var(--cian); color: #000; }
            .btn-dl { background: #2ecc71; color: #fff; display: none; text-decoration: none; }
            #preview { display: none; margin-top: 20px; }
            .thumb { width: 100%; border-radius: 10px; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TURBOLINK</h1>
            <input type="text" id="url" placeholder="Pega el link aquí...">
            <button class="btn btn-main" id="processBtn" onclick="process()">GENERAR DESCARGA</button>
            <div id="status" style="margin-top:10px;"></div>
            
            <div id="preview">
                <img id="img" class="thumb">
                <p id="timer">Esperando 12s...</p>
                <a id="dlLink" href="" class="btn btn-dl">DESCARGAR AHORA</a>
            </div>
        </div>

        <script>
            async function process() {
                const url = document.getElementById('url').value;
                const status = document.getElementById('status');
                const btn = document.getElementById('processBtn');
                
                status.innerText = "⏳ Analizando...";
                btn.disabled = true;

                try {
                    const r = await fetch('/api/get?url=' + encodeURIComponent(url));
                    const d = await r.json();
                    if(d.success) {
                        status.innerText = "✅ ¡Listo!";
                        document.getElementById('img').src = d.thumb;
                        document.getElementById('preview').style.display = 'block';
                        
                        let t = 12;
                        const timer = setInterval(() => {
                            t--;
                            document.getElementById('timer').innerText = "Activando en " + t + "s...";
                            if(t <= 0) {
                                clearInterval(timer);
                                document.getElementById('timer').style.display = 'none';
                                const dl = document.getElementById('dlLink');
                                dl.style.display = 'block';
                                // Importante: Enviamos a nuestra ruta de túnel
                                dl.href = "/api/download?v=" + encodeURIComponent(d.url);
                            }
                        }, 1000);
                    } else { status.innerText = "❌ Error: " + d.msg; btn.disabled = false; }
                } catch(e) { status.innerText = "❌ Error de conexión."; btn.disabled = false; }
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/api/get')
def get_info():
    url = get_clean_url(request.args.get('url'))
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": API_HOST, "Content-Type": "application/json"}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        data = r.json()
        dl_url = data.get('url') or (data.get('medias', [{}])[0].get('url'))
        if dl_url:
            return jsonify({"success": True, "url": dl_url, "thumb": data.get('thumbnail', '')})
    except: pass
    return jsonify({"success": False, "msg": "Video no disponible"})

@app.route('/api/download')
def download_tunnel():
    # ESTE ES EL TRUCO: Tu servidor Railway "descarga" el video y se lo pasa al usuario
    # Así Facebook cree que es una visita normal y permite la descarga
    video_url = request.args.get('v')
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=30)
        # Forzamos la descarga del archivo en el móvil/PC
        return Response(stream_with_context(r.iter_content(chunk_size=1024*1024)), 
                        content_type='video/mp4',
                        headers={'Content-Disposition': 'attachment; filename="TurboLink_Video.mp4"'})
    except:
        return "Error al procesar el video", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
