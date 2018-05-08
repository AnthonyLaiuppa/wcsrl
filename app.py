from flask import Flask, Response, request, render_template
from backend import apiBackend 


app = Flask(__name__)
api = apiBackend()
api.load_config()
roauth = api.get_roauth_url()

@app.route("/")
def index():	
    return render_template('index.html', roauth=roauth)

@app.route('/authd/', methods=['GET'])
def authd():
	token = request.args.get('code')
	api.set_user(token)
	links = api.get_links()
	return render_template('links.html', links=links)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8000)
