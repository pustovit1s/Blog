"""forms for blog application"""
from django import forms
from .models import Comment



class EmailPostForm(forms.Form):
    """class which create email recomendations form"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)



class CommentForm(forms.ModelForm):
    """class which create comments form"""
    class Meta:
        """meta class for import existing comment form"""
        model = Comment
        fields = ['name', 'email', 'body']



class SearchForm(forms.Form):
    """ class for creating search form"""
    query = forms.CharField()
