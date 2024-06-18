import json
import random
import torch
import torch.nn.functional as F
import transformers
from transformers import BertForSequenceClassification, BertTokenizerFast, pipeline, BertConfig

# Custom upcast_masked_softmax function without dim argument
def upcast_masked_softmax(x, mask, mask_value, scale, softmax_dtype):
    input_dtype = x.dtype
    x = x.to(softmax_dtype) * scale
    x = torch.where(mask, x, mask_value)
    x = F.softmax(x, -1).to(input_dtype)  # Explicitly use positional argument for dim
    return x

def load_json_file(filename):
    with open(filename) as f:
        file = json.load(f)
    return file

def get_chatbot_response(chatbot, text, intents, label2id):
    score = chatbot(text)[0]['score']
    if score < 0.7:
        return "Sorry, I can't answer that."
    else:
        label = chatbot(text)[0]['label']
        label_id = label2id.get(label, None)
        if label_id is None:
            return "Sorry, I don't have an answer for that."
        response = random.choice(intents['intents'][label_id].get('responses', ["Sorry, I don't have an answer for that."]))
        return response

# Initialize model and tokenizer
model_path = "chatbot"
# Load the configuration
config = BertConfig.from_pretrained(model_path)

# Load the model with the configuration
model = BertForSequenceClassification.from_pretrained(model_path, config=config)

# Load the tokenizer
tokenizer = BertTokenizerFast.from_pretrained(model_path)

# Define the pipeline manually
chatbot_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load intents from JSON file
filename = 'campus_qa.json'
intents = load_json_file(filename)

label2id = {
    'greeting': 0, 'goodbye': 1, 'creator': 2, 'name': 3, 'hours': 4,
    'number': 5, 'course': 6, 'fees': 7, 'location': 8, 'hostel': 9,
    'event': 10, 'document': 11, 'floors': 12, 'syllabus': 13,
    'library': 14, 'infrastructure': 15, 'canteen': 16, 'menu': 17,
    'placement': 18, 'principal': 19, 'CSE': 20, 'CAI': 21, 'AIDS': 22,
    'CSM': 23, 'ECE': 24, 'IOT': 25, 'EEE': 26, 'IT': 27, 'CIVIL': 28,
    'Mechanical Engineering': 29, 'Chairman': 30, 'sem': 31,
    'admission': 32, 'scholarship': 33, 'facilities': 34,
    'Google CodeLabs': 35, 'University Innovation Fellows': 36,
    'transport': 37, 'IUCEE': 38, 'SAC': 39, 'SAC SELECTIONS': 40,
    'clubs': 41, 'NCC': 42, 'NSS': 43, 'sports': 44, 'uniform': 45,
    'committee': 46, 'random': 47, 'swear': 48, 'vacation': 49,
    'salutation': 50, 'task': 51, 'ragging': 52, 'hod': 53
}

def message(text):
    response = get_chatbot_response(chatbot_pipeline, text, intents, label2id)
    return response

def chat(chatbot):
    print("Chatbot: Hi! I am your virtual assistant. Feel free to ask, and I'll do my best to provide you with answers and assistance.")
    print("Type 'quit' to exit the chat\n\n")

    text = input("User: ").strip().lower()

    while text != 'quit':
        response = get_chatbot_response(chatbot, text, intents, label2id)
        print(f"Chatbot: {response}\n\n")
        text = input("User: ").strip().lower()

if __name__ == "__main__":
    print("PyTorch version:", torch.__version__)
    print("Transformers version:", transformers.__version__)

    # Start the chatbot in interactive mode
    # chat(chatbot_pipeline)
    print(message("tell me about vvit"))