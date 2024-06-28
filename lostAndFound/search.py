from .mail import sendMailTo
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
from .models import LostItems,FoundItems

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', device_map=0)
model = BertModel.from_pretrained('bert-base-uncased')

# model.cuda()  # only for nvidia gpu users

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    return inputs

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def matchSentence(item,type):
    sentences = ""
    target_sentence = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
    inventory = None
    if type == 'lost':
        inventory = FoundItems.objects.all()
    elif type == "found":
        inventory = LostItems.objects.all()
    sentences = [(i, i.itemName+' '+i.itemType+" "+i.keywords+" "+i.description) for i in inventory]
    print(f"target sentence = {target_sentence} sentence = {sentences}")
    
    if sentences:
        encoded_target = encode_text(target_sentence)

        with torch.no_grad():
            target_output = model(**encoded_target)
            target_embedding = mean_pooling(target_output, encoded_target['attention_mask'])

        similarities = []

        for item, sentence in sentences:
            encoded_sentence = encode_text(sentence)
            with torch.no_grad():
                sentence_output = model(**encoded_sentence)
                sentence_embedding = mean_pooling(sentence_output, encoded_sentence['attention_mask'])
            
            similarity_score = cosine_similarity(target_embedding, sentence_embedding)[0][0]
            similarities.append([item, similarity_score])

        print(similarities)
        if similarities:
            similarities = [x for x in similarities if x[1] > 0.75 ]
            similarities.sort(key=lambda x:x[1])
            similarities = similarities[:5]
            return [x[0] for x in similarities]
        else:
            return False

def SearchItems(data):
    type = data.split('_')[0]

    model = 'LostItems' if type == 'lost' else 'FoundItems'

    item = f'{model}.objects.get(submissionID="{data}")'
    item = eval(item)

    values = matchSentence(item,type) 

    if not values:
        return False

    sendMailTo(item.email,item.submissionID,item.description,values)
    return True 
   
