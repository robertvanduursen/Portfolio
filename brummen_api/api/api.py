from flask import Flask
from flask import request
from flasgger import Swagger
from streets_view import streets

app = Flask(__name__)
api_docs = Swagger(app)


@app.route('/ipaddress', methods=['GET'])
def get_ip_address():
    """
    View your own IP address
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: The name to greet.
    responses:
      200:
        description: Your IP address
        schema:
          type: string
    """
    return f'Hello from {request.remote_addr}'


app.add_url_rule('/streets', 'streets', streets, methods=['GET'])


@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the Python API demo'


if __name__ == '__main__':
    app.run(debug=True)
