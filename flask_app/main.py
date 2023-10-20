from flask import Flask, render_template, jsonify

app = Flask(__name__)

counter = 0
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/demo', methods=['POST'])
def increment_counter():
    global counter
    counter += 1
    return jsonify({"new_count": "demo"})

if __name__ == '__main__':
    app.run(debug=True)
