from json import load
from flask import Flask, render_template, jsonify, Response, redirect, url_for, send_file, request
import speech_recognition as sr
import cv2
import io
from utils import identify_object
import spacy
from dotenv import load_dotenv
from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
load_dotenv()
print("Loading language tools")

load_dotenv()
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
r = sr.Recognizer()

print("Loading ML tools")
is_video_on = True

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

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


@app.route('/capture')
def capture():
    camera = cv2.VideoCapture(0)
    success, frame = camera.read()
    if success:
        pil_image = Image.fromarray(frame)
        return pil_image, 200
    else:
        return "Could not capture image", 500


@app.route('/toggle_video', methods=['POST'])
def toggle_video():
    global is_video_on
    is_video_on = not is_video_on
    print("in toggle!")
    return redirect(url_for('index'))


def get_api_result(image, question):
    inputs = processor(image, question, return_tensors="pt")
    out = model.generate(inputs["input_ids"],
                         pixel_values=inputs["pixel_values"])
    answer = processor.decode(out[0], skip_special_tokens=True)
    return answer

@app.route('/get_vqa_result', methods = ['POST'])
def get_vqa_res():
    image, status = capture()
    object_to_be_found = request.json['voice_input']
    print(object_to_be_found, " -- Object to be found")
    ml_model_result = get_api_result(image, object_to_be_found)
    return jsonify({"vqa_response": ml_model_result})



@app.route('/get_user_speech', methods=['POST'])
def get_user_speech():
    with sr.Microphone() as source:
        print('Please start speaking..\n')
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print(text)
        # obj_to_be_found = identify_object(nlp, text)
        print(f"Recognized text: {text}")
    return jsonify({"obj_to_be_found": text})
if __name__ == '__main__':
    app.run(debug=True)
