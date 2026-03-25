import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA
def get_ydl_opts():
    return {
        'proxy': "http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80",
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

# INTERFAZ PWA NEÓN
HTML_PWA = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor Pro 🚀</title>
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#0a0a0a">
    <meta name="apple-mobile-web-app-capable" content="yes">
    
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --success: #2ecc71; --dark: #0a0a0a; }
        body { background: var(--dark); color: #fff; font-family: sans-serif; margin: 0; padding: 20px; text-align: center; }
        .card { background: #151515; padding: 30px; border-radius: 25px; border: 1px solid #333; max-width: 450px; margin: auto; box-shadow: 0 10px 50px #000; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; font-weight: 900; }
        input { width: 100%; padding: 20px; border-radius: 15px; border: 1px solid #333; background: #222; color: #fff; margin: 20px 0; box-sizing: border-box; outline: none; }
        #btn { width: 100%; padding: 18px; background: #fff; color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; font-size: 16px; }
        .dl-btn { display: none; background: var(--success); color: white; padding: 20px; border-radius: 15px; text-decoration: none; margin-top: 20px; font-weight: bold; box-shadow: 0 0 20px var(--success); }
        #installBanner { display: none; background: var(--primary); color: #000; padding: 10px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div id="installBanner">📲 INSTALAR MOTOR PRO EN INICIO</div>
    
    <div class="card">
        <h1>MOTOR PRO</h1>
        <p style="font-size: 10px; color: #555;">PWA INSTALABLE • BOLIVIA 🇧🇴</p>
        <input type="text" id="urlInput" placeholder="Pega link de TikTok, FB o IG...">
        <button id="btn" onclick="procesar()">BUSCAR VIDEO</button>
        <div id="status" style="margin-top: 20px; color: #888;"></div>
        <a id="downloadBtn" class="dl-btn" href="#" target="_blank">📥 GUARDAR EN CELULAR</a>
    </div>

    <script>
        // Lógica de Instalación PWA
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('installBanner').style.display = 'block';
        });

        document.getElementById('installBanner').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') document.getElementById('installBanner').style.display = 'none';
                deferredPrompt = null;
            }
        });

        // Registro del Service Worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }

        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dl = document.getElementById('downloadBtn');
            const btn = document.getElementById('btn');
            
            if(!url) return;
            btn.disabled = true;
            dl.style.display = "none";
            status.innerHTML = "⏳ <span style='color:var(--primary)'>Extrayendo video...</span>";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await res.json();
                if(data.success) {
                    status.innerHTML = "✅ ¡Listo! <br>Haz clic abajo para guardar.";
                    dl.href = data.url;
                    dl.style.display = "block";
                } else {
                    status.innerText = "❌ Error: Video no encontrado.";
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
def home(): return render_template_string(HTML_PWA)

# ARCHIVOS NECESARIOS PARA PWA
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "name": "Motor Pro Bolivia",
        "short_name": "MotorPro",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#00f2ea",
        "icons": [{
            "src": "https://cdn-icons-png.flaticon.com/512/2583/2583130.png",
            "sizes": "512x512",
            "type": "image/png"
        }]
    })

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('fetch', function(event) {});", mimetype='application/javascript')

@app.route('/api/info')
def info():
    u = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            info = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": info['url']})
    except: return jsonify({"success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
