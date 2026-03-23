import os
import re
import yt_dlp
import random # Necesario para la autorrotación
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# (Tu variable HTML_PREMIUM se mantiene igual, no la toques)

@app.route('/')
def index():
    return render_template_string(HTML_PREMIUM)

@app.route('/api/extract')
def api_extract():
    url = request.args.get('url')
    fmt = request.args.get('type', 'mp4')
    
    if not url:
        return jsonify({"success": False, "error": "URL requerida"})

    # --- CONFIGURACIÓN DE TU "EJÉRCITO" DE PROXIES (Se mantiene igual) ---
    proxy_users = [
        "ksvyuzxs-8", "ksvyuzxs-1", "ksvyuzxs-2", "ksvyuzxs-3", 
        "ksvyuzxs-4", "ksvyuzxs-5", "ksvyuzxs-6", "ksvyuzxs-7", 
        "ksvyuzxs-9", "ksvyuzxs-10"
    ]
    proxy_pass = "r148qqniiwdz"
    proxy_host = "p.webshare.io"
    proxy_port = "80"

    # Intentamos rotar hasta que uno funcione
    for user in proxy_users:
        proxy_url = f"http://{user}:{proxy_pass}@{proxy_host}:{proxy_port}"
        
        ydl_opts = {
            'proxy': proxy_url,
            'quiet': True,
            'no_warnings': True,
            # --- LA SOLUCIÓN MÁGICA AL ERROR 403 ---
            # Esto usa cookies de un navegador virtual en el servidor.
            # No usa tus cookies personales, pero engaña a YouTube.
            'cookies_from_browser': 'chrome', 
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if fmt == 'mp4' else 'bestaudio[ext=m4a]/bestaudio',
            'nocheckcertificate': True,
            'geo_bypass': True,
            'match_filter': lambda info: None if info.get('duration', 0) <= 600 else 'Video muy largo (máx 10 min)',
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
                    # ¡Éxito! Devolvemos la respuesta
                    return jsonify({
                        "success": True,
                        "title": info.get('title', 'Video'),
                        "thumbnail": info.get('thumbnail'),
                        "url": link
                    })
        except Exception as e:
            # Si el error es por duración, no seguimos intentando
            if "muy largo" in str(e):
                return jsonify({"success": False, "error": "El video excede los 10 minutos."})
            # Si es el error 403 o similar, imprimimos el error en logs e intentamos con otro proxy
            print(f"Proxy {user} falló con error: {e}. Intentando con el siguiente...")
            continue

    return jsonify({"success": False, "error": "YouTube está bloqueando la conexión. Intenta de nuevo más tarde."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
