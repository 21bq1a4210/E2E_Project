from django.db import models
from uuid import uuid4

class LostIDField(models.Field):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def db_type(self,connection) :
        return 'varchar(100)'

    def from_db_value(self,value,connection,expression):
        return value
    
    def to_python(self,value):
        if not value:
            return value
        return str(value)
    
    def get_prep_value(self, value):
        return str(value) if value else None
    
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = "lost_"+str(uuid4())
            setattr(model_instance, self.attname, value)
        return value
    
class FoundIDField(models.Field):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def db_type(self,connection) :
        return 'varchar(100)'

    def from_db_value(self,value,connection,expression):
        return value
    
    def to_python(self,value):
        if not value:
            return value
        return str(value)
    
    def get_prep_value(self, value):
        return str(value) if value else None
    
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = "found_"+str(uuid4())
            setattr(model_instance, self.attname, value)
        return value
    

class LostItems(models.Model):
    submissionID = LostIDField(max_length = 100)
    name = models.CharField(max_length=200, default=None)
    email = models.EmailField(max_length=50,default=None)
    contact = models.BigIntegerField(max_length=50,default=None)
    itemName = models.CharField(max_length=200, default=None)
    itemType = models.CharField(max_length=200, default=None)
    keywords = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=100, default=None)
    time = models.TimeField(max_length=200, default=None)
    date = models.DateField(max_length=200, default=None)
    image = models.ImageField(max_length=200,null=True, blank=True, upload_to='lostitems/')
    description = models.TextField( default=None)

class FoundItems(models.Model):
    submissionID = FoundIDField(max_length = 100)
    name = models.CharField(max_length=200, default=None)
    email = models.EmailField(max_length=50,default=None)
    contact = models.BigIntegerField(max_length=50,default=None)
    itemName = models.CharField(max_length=200, default=None)
    itemType = models.CharField(max_length=200, default=None)
    keywords = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=100, default=None)
    time = models.TimeField(max_length=200, default=None)
    date = models.DateField(max_length=200, default=None)
    image = models.ImageField(max_length=200,null=True, blank=True, upload_to='founditems/')
    description = models.TextField(default=None)
