from flask import Flask, render_template, jsonify, Response, redirect, url_for
import speech_recognition as sr
import cv2

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

@app.route('/toggle_video', methods=['POST'])
def toggle_video():
    global is_video_on
    is_video_on = not is_video_on
    return redirect(url_for('index'))


@app.route('/get_user_speech', methods=['POST'])
def increment_counter():
    with sr.Microphone() as source:
        print('Please start speaking..\n')
        audio = r.listen(source)
        text = r.recognize_google(audio)
        print(f"Recognized text: {text}")

    return jsonify({"new_count":text})
if __name__ == '__main__':
    app.run(debug=True)
