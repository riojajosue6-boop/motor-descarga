import os
import requests
from flask import Flask, request, jsonify, render_template_string, Response, stream_with_context

app = Flask(__name__)

# --- CONFIGURACIÓN ---
API_KEY = "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585"
API_HOST = "auto-download-all-in-one.p.rapidapi.com"

user_stats = {} 

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TurboLink 🚀 | Descargas Pro</title>
    <style>
        :root { --primary: #00f2ea; --bg: #0a0a0a; --card: #151515; }
        body { background: var(--bg); color: #fff; font-family: sans-serif; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 500px; margin: auto; background: var(--card); padding: 30px; border-radius: 25px; border: 1px solid #333; }
        h1 { color: var(--primary); font-size: 32px; text-transform: uppercase; margin-bottom: 5px; }
        input { width: 100%; padding: 18px; border-radius: 15px; border: 2px solid #222; background: #1a1a1a; color: #fff; box-sizing: border-box; margin: 20px 0; }
        #mainBtn { width: 100%; padding: 18px; background: var(--primary); color: #000; border: none; border-radius: 15px; font-weight: 900; cursor: pointer; }
        #mainBtn:disabled { background: #333; color: #666; }
        #timer-msg { display: none; margin-top: 20px; padding: 15px; border: 1px dashed var(--primary); border-radius: 15px; }
        .dl-box { background: #2ecc71; color: #000; padding: 20px; border-radius: 15px; margin-top: 20px; }
        .dl-btn { background: #000; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 10px; font-weight: bold; display: inline-block; margin-top: 10px; border:none; cursor:pointer;}
        .stats { margin-top: 25px; font-size: 12px; color: #555; display: flex; justify-content: space-around; }
    </style>
</head>
<body>
    <div class="container">
        <h1>TURBOLINK</h1>
        <p style="color:#666; font-size:12px; font-weight:bold;">MODO PROTECCIÓN ACTIVO 🛡️</p>
        <input type="text" id="urlInput" placeholder="Pega el link aquí...">
        <button id="mainBtn" onclick="startProcess()">Arrancar Motor</button>
        <div id="timer-msg">
            🚀 Optimizando motor... <h2 id="countdown" style="color:var(--primary);">15</h2>
        </div>
        <div id="status"></div>
        <div class="stats">
            <span>Redes: <b id="stat-social" style="color:#fff">0/4</b></span>
            <span>YouTube: <b id="stat-yt" style="color:#fff">0/3</b></span>
        </div>
    </div>

    <script>
        async function startProcess() {
            const url = document.getElementById('urlInput').value.trim();
            if(!url) return alert("Pega un link");
            const btn = document.getElementById('mainBtn');
            const timerMsg = document.getElementById('timer-msg');
            const status = document.getElementById('status');
            btn.disabled = true; status.innerHTML = ""; timerMsg.style.display = "block";
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
            status.innerHTML = "⏳ Extrayendo...";
            try {
                const response = await fetch('/api/fetch?url=' + encodeURIComponent(url));
                const data = await response.json();
                if(data.success) {
                    document.getElementById('stat-social').innerText = data.stats.social + "/4";
                    document.getElementById('stat-yt').innerText = data.stats.yt + "/3";
                    
                    let dlUrl = data.method === "tunnel" ? `/api/download_tunnel?video_url=${encodeURIComponent(data.download_url)}` : data.download_url;
                    
                    status.innerHTML = `
                        <div class="dl-box">
                            <p style="margin:0; font-weight:bold;">✅ ¡Video Listo!</p>
                            <a href="${dlUrl}" class="dl-btn" download="video.mp4">📥 DESCARGAR AHORA</a>
                        </div>`;
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
    user_ip = request.remote_addr
    if user_ip not in user_stats: user_stats[user_ip] = {'yt': 0, 'social': 0}
    is_yt = "youtube.com" in url or "youtu.be" in url
    is_tiktok = "tiktok.com" in url
    
    if is_yt and user_stats[user_ip]['yt'] >= 3: return jsonify({"success": False, "message": "Límite YT."})
    if not is_yt and user_stats[user_ip]['social'] >= 4: return jsonify({"success": False, "message": "Límite Redes."})

    headers = {"content-type": "application/json", "x-rapidapi-host": API_HOST, "x-rapidapi-key": API_KEY}
    try:
        r = requests.post(f"https://{API_HOST}/v1/social/autolink", json={"url": url}, headers=headers, timeout=15)
        res = r.json()
        video_url = res.get('url')
        if video_url:
            if is_yt: user_stats[user_ip]['yt'] += 1
            else: user_stats[user_ip]['social'] += 1
            return jsonify({"success": True, "download_url": video_url, "stats": user_stats[user_ip], "method": "tunnel" if is_tiktok else "redirect"})
        return jsonify({"success": False, "message": "No encontrado."})
    except: return jsonify({"success": False, "message": "Error API."})

@app.route('/api/download_tunnel')
def download_tunnel():
    video_url = request.args.get('video_url')
    # Añadimos Headers para que TikTok no nos bloquee
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        req = requests.get(video_url, headers=headers, stream=True, timeout=30)
        # Si la respuesta no es 200 (OK), hay un error
        if req.status_code != 200:
            return "Error: TikTok bloqueó el acceso.", 403
            
        def generate():
            for chunk in req.iter_content(chunk_size=8192): yield chunk
            
        response = Response(stream_with_context(generate()), content_type='video/mp4')
        response.headers['Content-Disposition'] = 'attachment; filename="TurboLink_Video.mp4"'
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
