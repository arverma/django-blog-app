from django import forms
from .models import Post

class Synthetic_Form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
