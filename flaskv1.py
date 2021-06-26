# import main Flask class and request object
from flask import Flask, request
from flask_cors import CORS
import json

# create the Flask app
app = Flask(__name__)
CORS(app)

@app.route('/query-example')
def query_example():
    return 'Query String Example'

@app.route('/form-example', methods=['POST', 'GET'])
def form_example():
    if request.method == 'POST':
        request_file = request.files.get('video')
        request_stamps = json.loads(request.form.get('timestamps'))
        request_data = json.loads(request.form.get('data'))
     
        print("elapsed time: {}".format(int(int(request_stamps["stop"])-int(request_stamps["start"]))/1000))
        print(request_file)
        print(len(request_data))
        
    return 'Form Data Example'

@app.route('/json-example', methods=['POST', 'GET'])
def json_example():

    request_data = request.get_json()
    print(request_data)
    return 'JSON Object Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)