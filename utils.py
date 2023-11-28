
def identify_object(nlp, sentence):
    doc = nlp(sentence.lower())
    for token in doc:
        if "obj" in token.dep_:
            return token.text
        
    
    