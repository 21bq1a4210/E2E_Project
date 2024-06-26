from .models import LostItems,FoundItems
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank,TrigramSimilarity
from .mail import sendMailTo
from .bertSearch import matchSentence

def SearchItems(data):
    item = None
    type = data.split('_')[0]
    if type == 'lost':
        item = LostItems.objects.get(submissionID = data)
        listOfIds = matchSentence(item,type)
        values = [FoundItems.objects.get(submissionID = x) for x in listOfIds]
        # query = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
        # vector = SearchVector('itemName',
        #                 'itemType',
        #                 'keywords',
        #                 'location',
        #                 'time',
        #                 'date',
        #                 'description')
        # results = FoundItems.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        # values = list(results.values())
        if len(values) == 0:
            print(1)
            return False
        else:
            print(2)
            sendMailTo(item.email,item.submissionID,item.description,values)
            return True
    elif type == 'found':
        item = FoundItems.objects.get(submissionID = data)
        listOfIds = matchSentence(item,type)
        values = [LostItems.objects.get(submissionID = x) for x in listOfIds]
        # query = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
        # vector = SearchVector('itemName',
        #                 'itemType',
        #                 'keywords',
        #                 'location',
        #                 'time',
        #                 'date',
        #                 'description')
        # results = LostItems.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        # values = list(results.values())
        if len(values) == 0:
            print(1)
            return False
        else:
            print(2)
            sendMailTo(item.email,item.submissionID,item.description,values)
            return True
        

    return False


