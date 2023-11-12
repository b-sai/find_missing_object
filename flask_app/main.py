from json import load
from flask import Flask, render_template, jsonify, Response, redirect, url_for, send_file, request
import speech_recognition as sr
import cv2
import io
from utils import identify_object
import spacy
from dotenv import load_dotenv
import replicate
load_dotenv()
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
r = sr.Recognizer()

counter = 0
@app.route('/')
def index():
    return render_template('index.html', is_video_on = is_video_on)

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

is_video_on = False

@app.route('/capture')
def capture():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    if success:
        cv2.imwrite('C:/Users/bsais/Desktop/image.jpg', frame)  
        return "Frame captured and saved successfully", 200
    else:
        return "Could not capture image", 500


@app.route('/toggle_video', methods=['POST'])
def toggle_video():
    global is_video_on
    is_video_on = not is_video_on
    return redirect(url_for('index'))

def get_api_result(obj_to_be_found):
    image_path = 'C:/Users/bsais/Desktop/image.jpg'
    output = replicate.run(
        "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
        input={"image": open(image_path, "rb"),
               'prompt': f'Please describe where {obj_to_be_found} is in this image'}
    )
    llava_response = "" 
    for item in output:
        llava_response+=item
    return llava_response

@app.route('/get_vqa_result', methods = ['POST'])
def get_vqa_res():
    # capture()
    object_to_be_found = request.json['voice_input']
    print(object_to_be_found, "Object to be found")
    ml_model_result = get_api_result(object_to_be_found)
    return jsonify({"vqa_response": ml_model_result})



@app.route('/get_user_speech', methods=['POST'])
def get_user_speech():
    with sr.Microphone() as source:
        print('Please start speaking..\n')
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)
        obj_to_be_found = identify_object(nlp, text)
        print(f"Recognized text: {obj_to_be_found}")
    return jsonify({"obj_to_be_found": obj_to_be_found})
if __name__ == '__main__':
    app.run(debug=True)
