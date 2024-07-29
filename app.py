from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    # Validate and extract URL
    pattern = r'https:\/\/[^?]+(?:\?[^&]*&)?expiry=(\d+)'
    match = re.search(pattern, url)
    if match:
        full_url = match.group(0)
        expiry_value = match.group(1)
        
        # Perform video download
        response = requests.get(full_url, stream=True)
        if response.status_code == 200:
            filename = 'video.mp4'
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return jsonify({'message': 'Download complete. File saved as video.mp4.'})
        else:
            return jsonify({'message': 'Failed to fetch the video.'}), 400
    else:
        return jsonify({'message': 'Invalid URL.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
