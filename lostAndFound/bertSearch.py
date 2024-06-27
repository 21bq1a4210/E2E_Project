from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
from .models import LostItems,FoundItems

# Load pre-trained model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    return inputs

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

# text_1 = "Example sentence one."
# text_2 = "Example sentence two."

# encoded_text_1 = encode_text(text_1)
# encoded_text_2 = encode_text(text_2)
# with torch.no_grad():
#     outputs_1 = model(**encoded_text_1)
#     outputs_2 = model(**encoded_text_2)

# # Get the embeddings from the last hidden state
# embeddings_1 = outputs_1.last_hidden_state
# embeddings_2 = outputs_2.last_hidden_state

# # Perform mean pooling
# sentence_embedding_1 = mean_pooling(outputs_1, encoded_text_1['attention_mask'])
# sentence_embedding_2 = mean_pooling(outputs_2, encoded_text_2['attention_mask'])

# similarity = cosine_similarity(sentence_embedding_1, sentence_embedding_2)
# print(f"Similarity score: {similarity[0][0]}")
def matchSentence(item,type):
    # sentences = ["This is a sample sentence.", "Another example sentence.", "A completely different text."]
    # target_sentence = "Sample sentence to match."
    sentences = ""
    target_sentence = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
    inventory = None
    if type == 'lost':
        inventory = FoundItems.objects.all()
    elif type == "found":
        inventory = LostItems.objects.all()
    sentences = [(i, i.itemName+' '+i.itemType+" "+i.keywords+" "+i.description +'@'+i.submissionID) for i in inventory]
    print(f"target sentence = {target_sentence} sentence = {sentences}")
    
    if sentences != []:
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
            similarities.append([item, sentence, similarity_score])

        # Find the most similar sentence
        print(similarities)
        if similarities != []:
            similarities = [x for x in similarities if x[2] > 0.6 ]
            similarities.sort(key=lambda x:x[2])
            similarities = similarities[:5]
            return [x[0] for x in similarities]
        else:
            return False
        # most_similar_sentence = max(similarities, key=lambda item: item[1])
        # print(f"Most similar sentence: {most_similar_sentence[0]} with similarity score: {most_similar_sentence[1]}")

