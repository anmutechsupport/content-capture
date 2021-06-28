# import main Flask class and request object
from flask import Flask, request, make_response
from flask_cors import CORS
import pickle
import json
import werkzeug
import cv2

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
     
        # print("elapsed time: {}".format(int(int(request_stamps["stop"])-int(request_stamps["startStream"]))/1000))
        print(request_file)
        print(request_stamps)
        print(len(request_data))

        # request_file.save('test.mp4')

        # request_file.seek(0)
        # video = cv2.VideoCapture(request_file.name)
        # while video.isOpened():
        #     ret, frame = video.read()
        #     if ret:
        #     # For testing purpose
        #         cv2.imshow("frame", frame)
        #     if cv2.waitKey(25) == ord('q'):
        #         print("nice")
        #         break
        #   ##############################
        #     # temp_file = TemporaryFile()
        #     # np.save(temp_file, frame)
        #     # temp_file.seek(0)
        #     # upload_to_some_where(temp_file.read())
        #     # temp_file.close()
        #     else:
        #         break
        # video.release()
        # request_file.close()

        # Note: when the request objects are saved, page refreshes
                
        # with open(f"bapeeg.pkl", "wb") as outfile:
        #     pickle.dump(request_data, outfile)
        
        # with open(f"timestamps.pkl", "wb") as outfile:
        #     pickle.dump(request_stamps, outfile)

        # with open(f"videoFile.pkl", "wb") as outfile:
        #     pickle.dump(request_file, outfile)

    return 'Form Data Example'

@app.route('/json-example', methods=['POST', 'GET'])
def json_example():

    request_data = request.get_json()
    print(request_data)
    return 'JSON Object Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)