import os
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context

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
        h1 { color: var(--primary); text-transform: uppercase; text-shadow: 0 0 10px var(--primary); }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; }
        button { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: bold; cursor: pointer; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; }
        .dl-box { background: #2ecc71; color: #000; padding: 25px; border-radius: 20px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 15px 30px; text-decoration: none; border-radius: 12px; font-weight: bold; display: block; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">GENERAR VIDEO MP4</button>
        <div id="timer-msg">🚀 Forzando motor de descarga... <h2 id="countdown" style="color:var(--primary);">15</h2></div>
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
            status.innerHTML = "⏳ Extrayendo datos...";
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    // LLAMAMOS AL TÚNEL INTERNO DE RAILWAY
                    const tunnelUrl = `/api/download?video_url=${encodeURIComponent(data.download_url)}`;
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-weight:bold;">✅ ¡ESTA VEZ SÍ!</p>
                            <a href="${tunnelUrl}" class="dl-btn" download="TurboLink_Video.mp4">📥 GUARDAR VIDEO</a>
                            <p style="font-size:10px; margin-top:10px;">Si la descarga no inicia sola, haz clic en el botón negro.</p>
                        </div>`;
                    window.location.href = tunnelUrl;
                } else { status.innerHTML = "❌ " + data.message; }
            } catch(e) { status.innerHTML = "❌ Error en el motor."; }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/fetch')
def fetch_link():
    url = request.args.get('url')
    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            return jsonify({"success": True, "download_url": video_url})
        return jsonify({"success": False, "message": "No se pudo extraer el video."})
    except: return jsonify({"success": False, "message": "Error de conexión."})

@app.route('/api/download')
def download_video():
    video_url = request.args.get('video_url')
    if not video_url: return "Falta URL", 400
    
    # DISFRAZAMOS LA PETICIÓN DESDE RAILWAY
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        req = requests.get(video_url, headers=headers, stream=True, timeout=30)
        
        # FORZAMOS AL NAVEGADOR A TRATARLO COMO VIDEO DESCARGABLE
        def generate():
            for chunk in req.iter_content(chunk_size=1024*1024): # 1MB chunks
                yield chunk
        
        response = Response(stream_with_context(generate()), content_type=req.headers.get('content-type'))
        response.headers['Content-Disposition'] = 'attachment; filename="TurboLink_Video.mp4"'
        return response
    except Exception as e:
        return f"Error en el túnel: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
