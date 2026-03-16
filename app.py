from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pytube import YouTube
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/descargar', methods=['GET'])
def descargar():
    url = request.args.get('url')
    tipo = request.args.get('tipo')
    
    if not url:
        return jsonify({"error": "No URL"}), 400

    try:
        yt = YouTube(url)
        tmpdir = tempfile.gettempdir()
        
        if tipo == 'mp3':
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        archivo = stream.download(output_path=tmpdir)
        return send_file(archivo, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
