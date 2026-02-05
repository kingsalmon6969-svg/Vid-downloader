import os
from flask import Flask, render_template, request, jsonify
import yt_dlp

# Force Flask to look in the correct directory for Replit
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

def get_video_info(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "success": True,
                "title": info.get('title', 'Unknown'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration_string', 'N/A'),
                "uploader": info.get('uploader', 'Unknown'),
                "download_url": info.get('url'),
                "extension": info.get('ext', 'mp4')
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    if not os.path.exists(os.path.join(template_dir, 'index.html')):
        return f"Error: Move index.html into a folder named 'templates'. Current path: {template_dir}"
    return render_template('index.html')

@app.route('/fetch', methods=['POST'])
def fetch_video():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"success": False, "error": "No URL"}), 400
    return jsonify(get_video_info(data['url']))

if __name__ == '__main__':
    # Fixed to port 5000 for Replit Webview
    print("Server launching on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
