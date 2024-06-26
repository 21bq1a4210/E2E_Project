from django import forms
from .models import LostItems,FoundItems

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItems
        fields = ['name', 
                  'email',
                  'contact',
                  'itemName',
                  'itemType',
                  'keywords',
                  'location',
                  'time',
                  'date',
                  'image',
                  'description']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItems
        fields = ['name', 
                  'email',
                  'contact',
                  'itemName',
                  'itemType',
                  'keywords',
                  'location',
                  'time',
                  'date',
                  'image',
                  'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }