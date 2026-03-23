import os
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# (Aquí va tu variable HTML_PREMIUM que ya tienes, no la cambies)

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/extract')
def api_extract():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    
    if not url:
        return jsonify({"success": False, "error": "Pega un link válido"})

    # --- CONFIGURACIÓN DE TU "EJÉRCITO" DE PROXIES ---
    # Ponemos el 8 (Francia) al principio como pediste
    proxy_users = [
        "ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", 
        "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", 
        "ksvyuzxs-9", "ksvyuzxs-10"
    ]
    proxy_pass = "r148qqniiwdz"
    proxy_host = "p.webshare.io"
    proxy_port = "80"

    # Intentamos con cada proxy de la lista hasta que uno responda
    for user in proxy_users:
        proxy_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        
        ydl_opts = {
            'proxy': proxy_url,
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if fmt == 'mp4' else 'bestaudio[ext=m4a]/bestaudio',
            'nocheckcertificate': True,
            'geo_bypass': True,
            'match_filter': lambda info: None if info.get('duration', 0) <= 600 else 'Video muy largo',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                link = info.get('url')
                
                if not link and 'formats' in info:
                    valid_formats = [f for f in info['formats'] if f.get('url')]
                    if valid_formats:
                        link = valid_formats[-1]['url']

                if link:
                    # ¡Éxito! Devolvemos la respuesta y salimos del bucle
                    return jsonify({
                        "success": True,
                        "title": info.get('title'),
                        "thumbnail": info.get('thumbnail'),
                        "url": link
                    })
        except Exception as e:
            # Si este proxy falla, el "continue" hace que intente con el siguiente de la lista
            print(f"Proxy {user} falló, intentando con el siguiente...")
            continue

    # Si llega aquí es porque TODOS los proxies fallaron (muy poco probable)
    return jsonify({"success": False, "error": "El servicio está saturado, intenta en un momento."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
