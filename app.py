import os
import yt_dlp
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CONFIGURACIÓN PROXY USA (Solo para "espiar" el link)
def get_ydl_opts():
    return {
        'proxy': "http://ksvyuzxs-us-rotate:r148qqniiwdz@p.webshare.io:80",
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

# INTERFAZ PWA DE ALTO IMPACTO
HTML_MASTER = '''
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
        body { background: var(--dark); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .card { background: #151515; padding: 40px 20px; border-radius: 30px; border: 1px solid #333; max-width: 480px; margin: 40px auto; box-shadow: 0 20px 60px #000; }
        h1 { background: linear-gradient(to right, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-size: 35px; font-weight: 900; }
        .badge { background: #222; color: var(--primary); padding: 5px 12px; border-radius: 20px; font-size: 10px; border: 1px solid var(--primary); display: inline-block; margin-bottom: 15px; }
        input { width: 100%; padding: 22px; border-radius: 18px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; outline: none; margin: 25px 0; font-size: 16px; }
        #btn { width: 100%; padding: 20px; background: #fff; color: #000; border: none; border-radius: 18px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        #btn:disabled { opacity: 0.3; }
        .dl-btn { display: none; background: var(--success); color: white; padding: 22px; border-radius: 18px; text-decoration: none; margin-top: 25px; font-weight: bold; font-size: 18px; display: none; box-shadow: 0 0 25px var(--success); }
        #installBanner { display: none; background: var(--primary); color: #000; padding: 15px; border-radius: 15px; margin-bottom: 20px; font-weight: bold; cursor: pointer; animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
    <div id="installBanner">📲 INSTALAR MOTOR PRO EN INICIO</div>
    
    <div class="card">
        <div class="badge">PWA CLOUD v3.0 ⚡</div>
        <h1>MOTOR PRO</h1>
        <p style="color:#555; font-size:12px; margin-top:5px; font-weight:bold;">BY JOSUE • COCHABAMBA 🇧🇴</p>
        
        <input type="text" id="urlInput" placeholder="Pega el link de TikTok aquí..." autocomplete="off">
        <button id="btn" onclick="procesar()">INICIAR DESCARGA</button>
        
        <div id="result">
            <p id="status" style="margin-top:25px; color:#aaa; font-size:14px;"></p>
            <a id="downloadBtn" class="dl-btn" href="#">📥 GUARDAR EN GALERÍA</a>
        </div>
    </div>

    <script>
        // --- LÓGICA DE INSTALACIÓN ---
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            document.getElementById('installBanner').style.display = 'block';
        });

        document.getElementById('installBanner').addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                deferredPrompt = null;
                document.getElementById('installBanner').style.display = 'none';
            }
        });

        // Registro de Service Worker para PWA
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }

        // --- LÓGICA DE DESCARGA "ANTI-403" ---
        async function procesar() {
            const url = document.getElementById('urlInput').value.trim();
            const status = document.getElementById('status');
            const dl = document.getElementById('downloadBtn');
            const btn = document.getElementById('btn');
            
            if(!url) return;
            btn.disabled = true;
            dl.style.display = "none";
            status.innerHTML = "⏳ <span style='color:var(--primary)'>Buscando enlace en USA...</span>";

            try {
                const res = await fetch('/api/info?url=' + encodeURIComponent(url));
                const data = await res.json();
                
                if(data.success) {
                    status.innerHTML = "📡 <span style='color:var(--success)'>¡Capturado! Transfiriendo video...</span>";
                    
                    // INTENTO DE DESCARGA POR BLOB (Túnel de memoria)
                    try {
                        const vRes = await fetch(data.url);
                        const blob = await vRes.blob();
                        const blobUrl = window.URL.createObjectURL(blob);
                        
                        dl.href = blobUrl;
                        dl.download = "motor_pro_video.mp4";
                        dl.style.display = "block";
                        status.innerHTML = "✅ <span style='color:lime'>¡LISTO PARA GUARDAR!</span>";
                        
                        // Disparo automático
                        dl.click();
                    } catch(e) {
                        // Si el navegador bloquea el túnel, damos el link directo pero con precaución
                        status.innerHTML = "⚠️ <span style='color:orange'>Mantén presionado el botón verde y elige 'Descargar vínculo'</span>";
                        dl.href = data.url;
                        dl.style.display = "block";
                    }
                } else {
                    status.innerHTML = "❌ <span style='color:var(--secondary)'>TikTok bloqueó el acceso.</span>";
                }
            } catch(e) {
                status.innerText = "❌ Error de conexión con Railway.";
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(HTML_MASTER)

# ARCHIVOS PARA PWA (OBLIGATORIOS)
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
    if "?" in u: u = u.split("?")[0]
    try:
        with yt_dlp.YoutubeDL(get_ydl_opts()) as ydl:
            info = ydl.extract_info(u, download=False)
            return jsonify({"success": True, "url": info['url']})
    except: return jsonify({"success": False})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
