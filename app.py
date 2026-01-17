from flask import Flask, send_from_directory, request
from api.get_gospel import handler

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('public', path)

@app.route('/api/get_gospel')
def get_gospel():
    date = request.args.get('date')
    result = handler({'date': date})
    return result['body'], result['statusCode']

if __name__ == '__main__':
    app.run(debug=True)