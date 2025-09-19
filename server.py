from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)
LOG_FOLDER = 'logs'

# Make sure log folder exists
os.makedirs(LOG_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_log():
    log_data = request.form.get('log', '')
    filename = f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(LOG_FOLDER, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(log_data)
    
    return "Log received!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
