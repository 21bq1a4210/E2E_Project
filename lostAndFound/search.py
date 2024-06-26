from .models import LostItems,FoundItems
from django.contrib.postgres.search import SearchQuery,SearchVector,SearchRank,TrigramSimilarity
from .mail import sendMailTo

def SearchItems(data):
    item = None
    type = data.split('_')[0]
    if type == 'lost':
        item = LostItems.objects.get(submissionID = data)
        query = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
        vector = SearchVector('itemName',
                        'itemType',
                        'keywords',
                        'location',
                        'time',
                        'date',
                        'description')
        # search_query = SearchQuery(query)

        # results = FoundItems.objects.annotate(
        #         similarity = SearchRank(vector, search_query) +
        #         TrigramSimilarity('description', query) +
        #         TrigramSimilarity('itemName', query) +
        #         TrigramSimilarity('itemType', query)+
        #         TrigramSimilarity('keywords',query)
        #         ).filter(similarity__gte=0.0001).order_by('-similarity')
        results = FoundItems.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        # return {
        #     'name' : results.values('name'),
        #     'contact' : results.values('contact')
        # }
        values = list(results.values())
        print(item)
        if len(values) == 0:
            print(1)
            return [type,False]
        else:
            print(2)
            sendMailTo(item.email,item.submissionID,item.description,values)
            return [type,True]
    elif type == 'found':
        item = FoundItems.objects.get(submissionID = data)
        query = item.itemName+' '+item.itemType+" "+item.keywords+" "+item.description
        vector = SearchVector('itemName',
                        'itemType',
                        'keywords',
                        'location',
                        'time',
                        'date',
                        'description')
        results = LostItems.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.0001).order_by('-rank')
        values = list(results.values())
        print(item.name)
        if len(values) == 0:
            print(1)
            return [type,False]
        else:
            print(2)
            sendMailTo(item.email,item.submissionID,item.description,values)
            return [type,True]
        

    return False


