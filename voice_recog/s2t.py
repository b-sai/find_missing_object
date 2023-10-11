from tkinter.tix import TEXT
import speech_recognition as sr
import spacy
import sys
import cv2
import torch
import os

parent_dir = os.path.dirname(os.getcwd())
sys.path.append(parent_dir)
from GroundingDINO.groundingdino.util.inference import load_model, load_image, predict, annotate

os.environ["CUDA_VISIBLE_DEVICES"] = ""

r = sr.Recognizer()
nlp = spacy.load("en_core_web_sm")

keyWord = 'alexa'

def preprocess_with_spacy(sentence):
    doc = nlp(sentence.lower())
    return [token.text for token in doc if not token.is_stop]

def identify_object(sentence):
    doc = nlp(sentence.lower())
    for token in doc:
        if "obj" in token.dep_:
            return token.text

text = ""
is_keyword_detected = False
with sr.Microphone() as source:
    print('Please start speaking..\n')
    audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"Recognized text: {text}")
        if keyWord.lower() in text.lower():
            print('Keyword detected in the speech.')
            is_keyword_detected = True
    except Exception as e:
        print(f"Exception occurred: {e}")
      
if is_keyword_detected:  
    print("1")
    text = text.lower()

    print("text", text)
    text = text[text.index(keyWord) + len(keyWord):]

    print(f"After keyword removal: {text}")

    preprocessed_text = preprocess_with_spacy(text)
    print(f"Preprocessed text: {preprocessed_text}")

    object_found = identify_object(text)
    print(f"Object identified: {object_found}")

    model = load_model(f"{parent_dir}/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py",
                       f"{parent_dir}/GroundingDINO/weights/groundingdino_swint_ogc.pth")
    
    IMAGE_PATH = "C:/Users/bsais/Downloads/bedroom.png"
    TEXT_PROMPT = object_found
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25

    image_source, image = load_image(IMAGE_PATH)

    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )

    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    cv2.imwrite("annotated_image.jpg", annotated_frame)

