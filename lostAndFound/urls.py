from django.urls import path
from . import views

urlpatterns = [
    path('lostandfound/',views.LostandFound, name='lostandfound'),
    path('lostandfound/lostform/',views.Lostform,name = 'Lostform'),
    path('lostandfound/foundform/',views.Foundform,name="Foundform"),
    path('lostandfound/searching/<str:id>',views.Searching,name="Searching"),
    path('lostandfound/search/',views.search,name="Search")

]