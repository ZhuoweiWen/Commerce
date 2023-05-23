from .choices import *
from django import forms
from django.forms import TextInput

class create_Form(forms.Form):
    name = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={'placeholder':'Enter the name of your listing','class':'form-control',
                'style':'margin-bottom:20px'}),
        label = "")
    price = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder':'Enter the starting bid of your listing', 'class':'form-control',
                'style':'margin-bottom:20px'}),
        label = "")
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Enter the description of your listing','class':'form-control',
                'style':'margin-bottom:20px'}),
        label = "")
    url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'placeholder':'Enter the url of the picture for your listing','class':'form-control',
                'style':'margin-bottom:20px'}),
        label = "")
    category = forms.ChoiceField(required=False,
            widget=forms.Select(), choices=CATEGORY_CHOICE)

class bid_Form(forms.Form):
    bid = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder':'Bid','class':'form-control',
                'style':'margin-top:10px'}),
        label = "")
    

class comment_Form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder':'Leave a comment','class':'form-control',
                'style':'margin-bottom:20px'}),
        label = "")
