import os
import time
from flask import Flask, request, jsonify, render_template_string, redirect

app = Flask(__name__)

# --- CONFIGURACIÓN DE SEGURIDAD Y MOTOR ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"

# Base de datos temporal en memoria (Se reinicia con el servidor)
user_stats = {} 

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀 | Descargas Pro</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 10px 50px rgba(0,0,0,0.8); }
        h1 { color: var(--primary); font-size: 32px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; }
        p.tagline { color: #666; font-size: 12px; margin-bottom: 30px; font-weight: bold; }
        
        .input-group { position: relative; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--primary); box-shadow: 0 0 15px var(--primary); }
        .clear-btn { position: absolute; right: 15px; top: 18px; color: #555; cursor: pointer; font-weight: bold; }

        button { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: 900; cursor: pointer; transition: 0.3s; text-transform: uppercase; }
        button:disabled { background: #333; color: #666; }
        
        #timer-msg { display: none; margin-top: 20px; padding: 15px; background: rgba(0,242,234,0.1); border-radius: 10px; border: 1px dashed var(--primary); font-size: 14px; color: #ccc; }
        .stats { margin-top: 25px; font-size: 12px; color: #555; display: flex; justify-content: space-around; }
        .footer { margin-top: 40px; font-size: 11px; color: #444; }
        .footer a { color: #666; text-decoration: none; margin: 0 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <p class="tagline">MULTIDOWNLOADER • CLOUD 🇧🇴</p>
        
        <div class="input-group">
            <input type="text" id="urlInput" placeholder="Pega el link aquí...">
            <span class="clear-btn" onclick="document.getElementById('urlInput').value=''">X</span>
        </div>

        <button id="mainBtn" onclick="startProcess()">Arrancar Motor</button>

        <div id="timer-msg">
            🚀 <span id="msg-text">Preparando motor...</span><br>
            <small>Por favor visita la publicidad, esto mantiene el servicio gratuito.</small>
            <h2 id="countdown" style="color:var(--primary); margin: 10px 0;">15</h2>
        </div>

        <div id="status" style="margin-top:20px; font-weight:bold;"></div>

        <div class="stats">
            <span>Redes: <b id="stat-social">0/4</b></span>
            <span>YouTube: <b id="stat-yt">0/3</b></span>
        </div>
    </div>

    <div class="footer">
        <a href="#">Privacidad</a> | <a href="#">Términos DMCA</a> | <a href="#">Contacto</a>
        <p>© 2026 TurboLink Bolivia - No almacenamos archivos.</p>
    </div>

    <script>
        let downloads = { social: 0, yt: 0 };

        async function startProcess() {
            const url = document.getElementById('urlInput').value;
            if(!url) return alert("Pega un link primero");

            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            const status = document.getElementById('status');
            const countDisplay = document.getElementById('countdown');

            // Lógica de espera (Peaje de Adsense)
            btn.disabled = true;
            status.innerHTML = "";
            timerMsg.style.display = "block";
            
            let timeLeft = 15;
            let timer = setInterval(async () => {
                timeLeft--;
                countDisplay.innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer);
                    timerMsg.style.display = "none";
                    await callAPI(url);
                    btn.disabled = false;
                }
            }, 1000);
        }

        async function callAPI(url) {
            const status = document.getElementById('status');
            status.innerHTML = "⏳ Extrayendo video...";
            
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = "✅ ¡Éxito! Redirigiendo...";
                    // Actualizar stats visuales
                    document.getElementById('stat-social').innerText = data.stats.social + "/4";
                    document.getElementById('stat-yt').innerText = data.stats.yt + "/3";
                    
                    // Redirección directa para ahorrar Ancho de Banda (Giga)
                    window.location.href = data.download_url;
                } else {
                    status.innerHTML = "❌ " + data.message;
                }
            } catch(e) {
                status.innerHTML = "❌ Error en el servidor.";
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/fetch')
def fetch_video():
    url = request.args.get('url')
    user_ip = request.remote_addr # Identificamos al usuario por IP
    
    # Inicializar contador si es nuevo
    if user_ip not in user_stats:
        user_stats[user_ip] = {'yt': 0, 'social': 0}
    
    is_yt = "youtube.com" in url or "youtu.be" in url
    
    # --- CONTROL DE TANQUE (LÍMITES) ---
    if is_yt and user_stats[user_ip]['yt'] >= 3:
        return jsonify({"success": False, "message": "Cupo de YouTube agotado por hoy."})
    if not is_yt and user_stats[user_ip]['social'] >= 4:
        return jsonify({"success": False, "message": "Cupo de Redes Sociales agotado."})

    # --- LLAMADA A LA API DE $9 ---
    import requests
    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "content-type": "application/json",
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    
    try:
        r = requests.post(api_url, json={"url": url}, headers=headers, timeout=15)
        res_data = r.json()
        
        # Simulamos verificación de peso (Escudo 25MB)
        # Nota: La mayoría de las APIs de video no dan el peso exacto antes,
        # pero configuramos el redirect para proteger tu Giga de banda ancha.
        
        if res_data.get('url'):
            # Sumar al contador
            if is_yt: user_stats[user_ip]['yt'] += 1
            else: user_stats[user_ip]['social'] += 1
            
            return jsonify({
                "success": True, 
                "download_url": res_data['url'],
                "stats": user_stats[user_ip]
            })
        else:
            return jsonify({"success": False, "message": "Video no encontrado o privado."})
            
    except Exception as e:
        return jsonify({"success": False, "message": "Error de conexión con el motor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
