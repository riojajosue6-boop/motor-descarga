import os
import requests
from flask import Flask, request, jsonify, render_template_string

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
    <title>TurboLink 🚀 | Descargas Pro Bolivia</title>
    <style>
        :root { --primary: #00f2ea; --secondary: #ff0050; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 10px 50px rgba(0,0,0,0.8); }
        h1 { color: var(--primary); font-size: 32px; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px var(--primary); }
        p.tagline { color: #666; font-size: 12px; margin-bottom: 30px; font-weight: bold; }
        
        .input-group { position: relative; margin-bottom: 20px; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; font-size: 16px; outline: none; transition: 0.3s; }
        input:focus { border-color: var(--primary); }
        .clear-btn { position: absolute; right: 15px; top: 18px; color: #555; cursor: pointer; font-weight: bold; z-index: 10; }

        #mainBtn { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: 900; cursor: pointer; transition: 0.3s; text-transform: uppercase; }
        #mainBtn:disabled { background: #333; color: #666; cursor: not-allowed; }
        
        #timer-msg { display: none; margin-top: 20px; padding: 20px; background: rgba(0,242,234,0.05); border-radius: 15px; border: 1px dashed var(--primary); }
        .stats { margin-top: 25px; font-size: 12px; color: #555; display: flex; justify-content: space-around; border-top: 1px solid #222; padding-top: 15px; }
        
        .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 15px; margin-top: 20px; animation: pulse 1.5s infinite; }
        .dl-btn { background: #000; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 10px; font-weight: bold; display: inline-block; margin-top: 10px; }
        
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.4); } 70% { box-shadow: 0 0 0 15px rgba(46, 204, 113, 0); } 100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); } }
        .footer { margin-top: 40px; font-size: 11px; color: #444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <p class="tagline">MOTOR DE DESCARGA PRO 🇧🇴</p>
        
        <div class="input-group">
            <input type="text" id="urlInput" placeholder="Pega el link de TikTok, YT, FB o IG...">
            <span class="clear-btn" onclick="document.getElementById('urlInput').value=''; document.getElementById('status').innerHTML='';">X</span>
        </div>

        <button id="mainBtn" onclick="startProcess()">Arrancar Motor</button>

        <div id="timer-msg">
            <span id="msg-text">🚀 Optimizando enlace para descarga...</span><br>
            <small style="color:var(--primary)">Visita la publicidad para mantener este servicio GRATIS.</small>
            <h2 id="countdown" style="color:var(--primary); margin: 15px 0; font-size: 40px;">15</h2>
        </div>

        <div id="status"></div>

        <div class="stats">
            <span>Redes Sociales: <b id="stat-social" style="color:#fff">0/4</b></span>
            <span>YouTube: <b id="stat-yt" style="color:#fff">0/3</b></span>
        </div>
    </div>

    <div class="footer">
        <p>TurboLink no almacena videos. Cumplimos con la DMCA y regulaciones legales.</p>
        <a href="#" style="color:#666">Privacidad</a> | <a href="#" style="color:#666">Términos</a>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Por favor, pega un enlace válido.");

            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            const status = document.getElementById('status');
            const countDisplay = document.getElementById('countdown');

            btn.disabled = true;
            status.innerHTML = "";
            timerMsg.style.display = "block";
            
            let timeLeft = 15;
            countDisplay.innerText = timeLeft;
            
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
            status.innerHTML = "⏳ <span style='color:var(--primary)'>Extrayendo video sin marca de agua...</span>";
            
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-weight:bold;">✅ ¡Video listo para descargar!</p>
                            <a href="${data.download_url}" target="_blank" rel="noopener noreferrer" class="dl-btn">
                                📥 GUARDAR EN DISPOSITIVO
                            </a>
                            <p style="font-size:10px; margin-top:10px; color:#000;">Si no inicia, mantén presionado el botón y elige "Descargar vínculo".</p>
                        </div>`;
                    
                    document.getElementById('stat-social').innerText = data.stats.social + "/4";
                    document.getElementById('stat-yt').innerText = data.stats.yt + "/3";
                } else {
                    status.innerHTML = "<p style='color:var(--secondary); margin-top:20px;'>❌ " + data.message + "</p>";
                }
            } catch(e) {
                status.innerHTML = "<p style='color:var(--secondary); margin-top:20px;'>❌ Error de conexión con el motor Turbo.</p>";
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
    user_ip = request.remote_addr
    
    if user_ip not in user_stats:
        user_stats[user_ip] = {'yt': 0, 'social': 0}
    
    is_yt = "youtube.com" in url or "youtu.be" in url
    
    # --- CONTROL DE LÍMITES (7 TOTAL) ---
    if is_yt and user_stats[user_ip]['yt'] >= 3:
        return jsonify({"success": False, "message": "Límite de YouTube alcanzado (3/3)."})
    if not is_yt and user_stats[user_ip]['social'] >= 4:
        return jsonify({"success": False, "message": "Límite de Redes alcanzado (4/4)."})

    api_url = "https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink"
    headers = {
        "content-type": "application/json",
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    
    try:
        r = requests.post(api_url, json={"url": url}, headers=headers, timeout=15)
        res_data = r.json()
        
        # Obtenemos la URL de descarga
        video_url = res_data.get('url')
        
        if video_url:
            # Sumar al contador solo si hubo éxito
            if is_yt: user_stats[user_ip]['yt'] += 1
            else: user_stats[user_ip]['social'] += 1
            
            return jsonify({
                "success": True, 
                "download_url": video_url,
                "stats": user_stats[user_ip]
            })
        else:
            return jsonify({"success": False, "message": "No se pudo obtener el link. Verifica que el video sea público."})
            
    except Exception as e:
        return jsonify({"success": False, "message": "Error en la API. Intenta más tarde."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
