# import main Flask class and request object
from flask import Flask, request, make_response, send_file, abort, send_from_directory
from flask_cors import CORS
import json
import tempfile
from video_parsing import parse_video
from parsing_EEG import predict
from cleanup import FileRemover
import os

# create the Flask app
app = Flask(__name__) # static_url_path=('/Users/anush/AppData/Local/Temp')
CORS(app)

@app.route('/form-example', methods=['POST', 'GET'])
def form_example():
    if request.method == 'POST':

        fileremover = FileRemover()

        request_file = request.files.get('video')
        request_stamps = json.loads(request.form.get('timestamps'))
        request_data = json.loads(request.form.get('data'))

        # print("elapsed time: {}".format(int(int(request_stamps["stop"])-int(request_stamps["startStream"]))/1000))
        # print(request_file)
        # print(request_stamps)
        # print(len(request_data))

        # request_file.save('test.mp4')

        # Note: when the request objects are saved, page refreshes
        # Note: file.read() returns bin, file.stream returns a spooledtempfile
                
        # with open(f"bapeeg.pkl", "wb") as outfile:
        #     pickle.dump(request_data, outfile)
        
        # with open(f"timestamps.pkl", "wb") as outfile:
        #     pickle.dump(request_stamps, outfile)

        # features = predict(request_data, request_stamps)
        # features = predict()

        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp:
            # print(temp.name)
            temp.write(request_file.read())
            temp.seek(0)
            # newfile = parse_video(temp, features)
            newfile, timestamps = parse_video(temp)
            newfile.seek(0)
            
            rel_path = os.path.relpath(newfile.name, tempfile.gettempdir())
            print(rel_path)
            try:
                # return send_file(newfile.name, as_attachment=True)
                resp = send_from_directory(tempfile.gettempdir(), rel_path, as_attachment=True)
                fileremover.cleanup_once_done(resp, newfile.name)

                return resp #as_attachment = True
            except FileNotFoundError:
                abort(404)

    return 'Form Data Example'

@app.route('/json-example', methods=['POST', 'GET'])
def json_example():

    request_data = request.get_json()
    print(request_data)
    return 'JSON Object Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)