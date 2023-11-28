# find_missing_object

Find objects by talking to a camera

## Instructions to Run

### Setup

**For Windows:**

```
git clone https://github.com/b-sai/find_missing_object.git
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py
```

**For Linux/Mac:**

```
git clone https://github.com/b-sai/find_missing_object.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py
```

NOTE: it might take about 5 minutes to install everything

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser after following above instructions