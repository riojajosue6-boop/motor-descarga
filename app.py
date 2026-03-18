import os
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
# Forzamos a que el JSON no destruya los acentos
app.config['JSON_AS_ASCII'] = False 
CORS(app)

HTML_FINAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Motor de Descarga</title>
    <style>
        body { background: #0f0f0f; color: white; font-family: sans-serif; text-align: center; padding: 50px; }
        .card { background: #1a1a1a; padding: 30px; border-radius: 15px; display: inline-block; border: 1px solid #333; }
        input { padding: 12px; width: 300px; border-radius: 5px; border: none; margin: 10px 0; background: #2a2a2a; color: white; }
        button { background: #cc0000; color: white; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        #status { margin-top: 20px; color: #ff4444; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 Motor de Descarga</h1>
        <input type="text" id="link" placeholder="Pega el link aquí">
        <br>
        <button onclick="bajar()">DESCARGAR AHORA</button>
        <div id="status"></div>
    </div>
    <script>
        async function bajar() {
            const link = document.getElementById('link').value;
            const st = document.getElementById('status');
            if(!link) return;
            st.innerText = "⏳ Procesando...";
            try {
                // CAMBIO CLAVE: Usamos una ruta nueva para limpiar el cache
                const r = await fetch('/descargar_motor?url=' + encodeURIComponent(link));
                const d = await r.json();
                if(d.url) {
                    st.style.color = "#44ff44";
                    st.innerText = "✅ ¡Enlace listo!";
                    window.location.href = d.url;
                } else {
                    st.innerText = "❌ Error: " + (d.error || "No encontrado");
                }
            } catch(e) { st.innerText = "❌ Error de conexión"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_FINAL)

# Cambiamos el nombre de la ruta para que Render no use el cache viejo
@app.route('/descargar_motor')
def engine():
    u = request.args.get('url')
    if not u: return jsonify({"error": "Pega una URL"}), 400

    # Limpieza total de URL
    u = u.split('?')[0].split('&')[0]

    headers = {
        "x-rapidapi-key": "47df6ef77amshc35a5a164a0e928p191584jsn8260ed140585",
        "x-rapidapi-host": "auto-download-all-in-one.p.rapidapi.com"
    }

    try:
        # Petición a la API
        res = requests.post("https://auto-download-all-in-one.p.rapidapi.com/v1/social/autolink", 
                           json={"url": u}, headers=headers, timeout=20)
        data = res.json()
        
        links = data.get("result", [])
        if links:
            # Mandamos el primer link que encontremos
            return jsonify({"url": links[0]['url']})
        
        return jsonify({"error": "La API no encontró el video. Intenta con otro link."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
