# Voice Object Finder

Discover and identify objects using your voice with this innovative project. The Voice Object Finder leverages speech recognition, computer vision, and natural language processing to locate and describe objects captured by a camera.

## Features

- **Voice Interaction:** Initiate the search by speaking the object you want to find.
- **Live Video Stream:** Toggle the live video stream to visually inspect the surroundings.
- **Visual Question Answering (VQA):** To answer questions about the identified objects.

## Web Interface Preview

![Web Interface Preview](screenshots/preview.png)

## Setup

Follow these instructions to set up and run the Voice Object Finder on your local machine.

### Prerequisites

- Python 3.6 or later
- pip

### Installation

**Clone the repository:**

   ```
   git clone https://github.com/b-sai/find_missing_object.git
   cd find_missing_object
   ```
   
**Create a virtual environment:**

*For Windows:*

```
python -m venv venv
source venv/Scripts/activate
```

*For Linux/Mac:*

```
python -m venv venv
source venv/bin/activate
```

**Install dependencies:**

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

NOTE: it might take about 5 minutes to install everything

**Run the application:**

```
python main.py
```

Open http://127.0.0.1:5000/ in your browser after following the above instructions.



## Usage

Follow these steps to interact with the Voice Object Finder:

1. Toggle the live video stream using the "TOGGLE VIDEO" button.
2. Click the "LISTEN" button to initiate voice interaction.
3. Speak the name of the object you want to find.
4. The application will capture your speech and video, displaying the requested object description using Visual Question Answering (VQA).

  
## Code Overview
- main.py: Contains the main application code, including Flask routes for video streaming, capturing images, and handling user speech.
- utils.py: Defines a function for identifying objects in a sentence using spaCy.
- index.html: HTML template for the application's front-end, including buttons and video stream display.
- style.css: CSS stylesheet for styling the HTML elements.





