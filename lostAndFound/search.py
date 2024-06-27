from .models import LostItems,FoundItems
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank,TrigramSimilarity
from .mail import sendMailTo
from .bertSearch import matchSentence

def SearchItems(data):
    item = None
    type = data.split('_')[0]

    model = 'LostItems' if type == 'lost' else 'FoundItems'

    item = f'{model}.objects.get(submissionID="{data}")'
    item = eval(item)
    values = matchSentence(item,type) 

    if not values:
        return False

    sendMailTo(item.email,item.submissionID,item.description,values)
    return True 
   
