from utility.responses import RESPONSES,STATUSCODES
from utility.countries import COUNTRIES
import pickle
import transformers
import numpy as np
import ast
import re

def load_pkl_files():
    global tokenizer
    global model

    # with open("models/tokenizer.pkl", "rb") as token_file:
    #     tokenizer = pickle.load(token_file)

    # with open("models/model.pkl", "rb") as model_file:
    #     model = pickle.load(model_file)
    tokenizer = transformers.AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    model = transformers.AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")
    
    response_message={
        'message_id':'initialization_complete',
        'status_code':STATUSCODES.OK.value,
        'response_message' : RESPONSES.INITIALIZATION_COMPLETE.value
    }

    return response_message

emotions_dict = {
    0: 'admiration',
    1: 'amusement',
    2: 'anger',
    3: 'annoyance',
    4: 'approval',
    5: 'caring',
    6: 'confusion',
    7: 'curiosity',
    8: 'desire',
    9: 'disappointment',
    10: 'disapproval',
    11: 'disgust',
    12: 'embarrassment',
    13: 'excitement',
    14: 'fear',
    15: 'gratitude',
    16: 'grief',
    17: 'joy',
    18: 'love',
    19: 'nervousness',
    20: 'optimism',
    21: 'pride',
    22: 'realization',
    23: 'relief',
    24: 'remorse',
    25: 'sadness',
    26: 'surprise',
    27: 'neutral'
}

def classifier(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    logits = outputs.logits.detach()
 
    # Convert logits to a NumPy array
    logits_array = logits.numpy()
 
    # Apply softmax
    exp_logits = np.exp(logits_array)
    probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

    predicted_emotion = np.argmax(probs, axis=-1).item()
    return([emotions_dict[predicted_emotion]])

def floor_occurrence_index(letter=" ", input_string=""):
    length = len(input_string)
    half_length = length // 2
 
    for i in range(half_length - 1, -1, -1):
        if input_string[i] == letter:
            return i
    return 0

def add_emotion_markups(request):
    if request['country']==COUNTRIES.INDIA:
        file_name=COUNTRIES.INDIA.value+"_mappings.txt"
        with open(f'mappings/{file_name}', 'r') as file:
            content = file.read()
            mappings = ast.literal_eval(content)

    input_text=request['message']
    makeover=""
    
    delimiter_pattern = r'[.,]'
    delim=str(delimiter_pattern)[1:3]
    delimiters=[]
    for i in input_text:
        if i in delim:
            delimiters.append(i)
    input_text = re.split(delimiter_pattern, input_text)
    input_length=len(input_text)
    counter=0
    for text in input_text:
        counter=counter+1
        words = text.split(" ")
        words = [word for word in words if word]
        word_count = len(words)
        remaining_time=(5-(word_count%5))*150
        timetag=""
        if word_count<5 and remaining_time!=0:
            timetag='<break time="'+str(remaining_time)+'ms"/>'

        model_outputs = classifier(text)
        arranged_emotion=model_outputs
        picked_emotion=model_outputs[0]
        
        break_point=floor_occurrence_index(input_string=text)
        
        makeover += text[:break_point]
        
        if counter<2 or "gratitude" in picked_emotion or counter==input_length:
            makeover=makeover+mappings[picked_emotion][:-3]+',close_up"/>'
        else:
            makeover=makeover+mappings[picked_emotion]
        
        makeover += text[break_point:]
        
        if delimiters!=[]:
            makeover=makeover+delimiters.pop(0)+timetag

    output={
        "message_id":request['message_id'],
        "message":makeover,
        "status_code":STATUSCODES.OK.value,
        "response_message":RESPONSES.CONVERTED.value,
        "session_details":request['session_details'],
        }
    
    return output
