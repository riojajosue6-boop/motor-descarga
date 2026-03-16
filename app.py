from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/descargar', methods=['GET'])
def descargar():
    url = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url:
        return jsonify({"error": "URL no proporcionada"}), 400

    try:
        # 'm' es para usar el cliente móvil, que suele tener menos bloqueos
        yt = YouTube(url, on_progress_callback=on_progress, client='m')
        tmpdir = tempfile.gettempdir()
        
        if tipo == 'mp3':
            stream = yt.streams.get_audio_only()
        else:
            stream = yt.streams.get_highest_resolution()

        archivo = stream.download(output_path=tmpdir)
        return send_file(archivo, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Error de YouTube: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
