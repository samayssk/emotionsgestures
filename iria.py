from transformers import AutoTokenizer, AutoModelForSequenceClassification
import ast
import re
import torch
import pickle
# tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
# model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

# tokenizer = AutoTokenizer.from_pretrained("toke")
# model = AutoModelForSequenceClassification.from_pretrained("mode")

def floor_occurrence_index(letter=" ", input_string=""):
    length = len(input_string)
    half_length = length // 2

    for i in range(half_length - 1, -1, -1):
        if input_string[i] == letter:
            return i
    return 0

with open("tokenizer.pkl", "rb") as token_file:
    tokenizer = pickle.load(token_file)
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

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
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_emotion = torch.argmax(probs, dim=-1).item()
    print("Predicted Emotion:", predicted_emotion)
    return([emotions_dict[predicted_emotion]])

with open('mappings.txt', 'r') as file:
    content = file.read()
    mappings = ast.literal_eval(content)
print(mappings)

try:
    with open('input_text.txt', 'r',encoding='utf-8') as file:
        input_text = file.read()
    print(input_text)
except:
    input_text="input()"
makeover=""
text="Our confidence lies not only in our expertise but also in our unwavering belief in the power of innovation."
if input_text=="input()":
    while True:
        text=input("Enter your text:\n")
        print(text)
        if text=="exit()":
            break
        makeover=makeover+text
        model_outputs = classifier(text)
        print(model_outputs[0])
        arranged_emotion=model_outputs[0][0]
        picked_emotion=arranged_emotion[list(arranged_emotion.keys())[0]]
        makeover=makeover+mappings[picked_emotion]
else:
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

        print("------------------",text)
        #makeover=makeover+text
        model_outputs = classifier(text)
        print(model_outputs[0])
        arranged_emotion=model_outputs
        picked_emotion=model_outputs[0]


        break_point=floor_occurrence_index(input_string=text)
        makeover += text[:break_point]

        if counter < 2 or "gratitude" in picked_emotion or counter == input_length:
            print(picked_emotion)
            makeover = makeover + mappings[picked_emotion][:-3] + ',close_up"/>'
        else:
            makeover = makeover + mappings[picked_emotion]

        makeover += text[break_point:]


        #makeover=makeover+text
        if delimiters!=[]:
            makeover=makeover+delimiters.pop(0)+timetag

# tokenizer.save_pretrained("toke")
# model.save_pretrained("mode")

# with open("tokenizer.pkl", "wb") as token_file:
#     pickle.dump(tokenizer, token_file)
# with open("model.pkl", "wb") as model_file:
#     pickle.dump(model, model_file)

print(makeover)
with open('output_text.txt', 'w') as file:
    file.write(makeover)
