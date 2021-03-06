from django import forms
from .models import Category

class BidForm(forms.Form):
    bid = forms.DecimalField(min_value=0, decimal_places=2, label="Enter Bid")

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=1920, initial="Comment", widget=forms.Textarea)

class ListingForm(forms.Form):
    title = forms.CharField(max_length=128, label="Listing Title")
    description = forms.CharField(max_length=1920, widget=forms.Textarea, initial="Description")
    starting_bid = forms.DecimalField(min_value=0, decimal_places=2)
    image_url = forms.CharField(max_length=128)
    category = forms.ModelChoiceField(queryset=Category.objects.all())