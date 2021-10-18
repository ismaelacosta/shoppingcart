from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/welcome/<name>/<country>', methods=['GET'])
def welcome(name, country):
	return jsonify({'name':name,'country':country})

if __name__ == '__main__':
	app.run(debug=True)