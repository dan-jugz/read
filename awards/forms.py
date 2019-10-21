from django import forms
from .models import Review

# form to create a rating
class NewReviewForm(forms.ModelForm):
 
    class Meta:
        model=Review
        exclude=['post','judge']