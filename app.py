import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DE PROXIES (FORZADO PARA EVITAR 403) ---
def get_ydl_opts():
    # Usamos el usuario con rotación de Webshare
    user = "ksvyuzxs-rotate" 
    pw = "r148qqniiwdz"
    proxy = f"http://{user}:{pw}@p.webshare.io:80"
    
    return {
        'proxy': proxy,
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'nocheckcertificate': True,
        # Cambiamos a User-Agent de iPhone 15 para saltar el Varnish Cache
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
        'socket_timeout': 30,
        'referer': 'https://www.tiktok.com/', # Engañamos a TikTok diciendo que venimos de su propia web
    }

# [MANTENEMOS TODO TU HTML_TEMPLATE IGUAL QUE ANTES]
# Solo asegúrate de que el código de abajo (las rutas) sea este:

@app.route('/')
def home():
    # Aquí va el HTML_TEMPLATE que te pasé hace un momento
    return render_template_string(open('app.py', 'r').read().split('HTML_TEMPLATE = \'\'\'')[1].split('\'\'\'')[0])

@app.route('/api/info')
def info():
    u = request.args.get('url')
    if not u: return jsonify({"success": False})
    
    # Limpiamos el link de TikTok para evitar errores de rastreo
    if "tiktok.com" in u and "?" in u:
        u = u.split("?")[0]

    try:
        # Forzamos a yt-dlp a que use el proxy SÍ O SÍ
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            i = ydl.extract_info(u, download=False)
            # Buscamos la URL de video más limpia (sin marcas de agua si es posible)
            video_url = i.get('url') or i.get('formats')[0].get('url')
            return jsonify({
                "success": True, 
                "url": video_url, 
                "title": i.get('title', 'Video RRSS')
            })
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# Mantenemos las rutas de Privacidad, Términos y Ads.txt
@app.route('/privacidad')
def privacidad(): return "<h1>Política de Privacidad</h1><p>Tus datos están seguros.</p>"
@app.route('/terminos')
def terminos(): return "<h1>Términos de Uso</h1><p>Uso personal solamente.</p>"
@app.route('/ads.txt')
def ads_txt(): return Response("google.com, pub-8532381032470048, DIRECT, f08c47fec0942fa0", mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
