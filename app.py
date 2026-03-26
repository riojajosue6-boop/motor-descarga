import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"
user_stats = {} 

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀</title>
    <style>
        :root { --primary: #00f2ea; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; }
        h1 { color: var(--primary); text-transform: uppercase; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; }
        button { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; }
        .dl-box { background: #2ecc71; color: #000; padding: 25px; border-radius: 20px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 15px 30px; text-decoration: none; border-radius: 12px; font-weight: bold; display: block; margin-top: 15px; width: 100%; box-sizing: border-box; }
        .instruction { font-size: 13px; color: #333; margin-top: 15px; font-weight: bold; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">GENERAR VIDEO MP4</button>
        <div id="timer-msg">🚀 Preparando motor de video... <h2 id="countdown" style="color:var(--primary);">15</h2></div>
        <div id="status"></div>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Pega un link");
            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            btn.disabled = true; timerMsg.style.display = "block";
            let timeLeft = 15;
            let timer = setInterval(async () => {
                timeLeft--; document.getElementById('countdown').innerText = timeLeft;
                if(timeLeft <= 0) {
                    clearInterval(timer); timerMsg.style.display = "none";
                    await callAPI(url); btn.disabled = false;
                }
            }, 1000);
        }

        async function callAPI(url) {
            const status = document.getElementById('status');
            status.innerHTML = "⏳ Convirtiendo a MP4...";
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-size:18px; font-weight:bold;">✅ ¡MP4 LISTO!</p>
                            
                            <a href="${data.download_url}" 
                               download="TurboLink_Video.mp4" 
                               type="video/mp4"
                               target="_blank" 
                               class="dl-btn">
                                📥 GUARDAR VIDEO
                            </a>

                            <div class="instruction">
                                ⚠️ SI SE ABRE UNA WEB O APP:<br>
                                1. Mantén presionado el botón negro.<br>
                                2. Elige <b>"Descargar vínculo"</b>.<br>
                                <small>(Asegúrate que el nombre termine en .mp4)</small>
                            </div>
                        </div>`;
                } else { status.innerHTML = "❌ " + data.message; }
            } catch(e) { status.innerHTML = "❌ Error en el motor."; }
        }
    </script>
</body>
</html>
'''

@app.route('/api/fetch')
def fetch_link():
    url = request.args.get('url')
    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    try:
        # Pedimos explícitamente el link de descarga a la API
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        
        # En la mayoría de las redes, la API devuelve un link que caduca.
        # Intentamos capturar el link directo del video.
        video_url = res.get('url')
        
        if video_url:
            return jsonify({"success": True, "download_url": video_url})
        return jsonify({"success": False, "message": "No se pudo convertir a video."})
    except: return jsonify({"success": False, "message": "Error API."})

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
