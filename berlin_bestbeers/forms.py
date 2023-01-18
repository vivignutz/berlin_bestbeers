from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """
    Form for comments
    """
    class Meta:
        """Form fields"""
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        """Remove body label and add placeholder text"""
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['body'].widget.attrs['placeholder'] = 'Add a comment here:'


class PostForm(forms.ModelForm):
    """
    Form for posts
    """
    class Meta:
        """Form fields"""
        model = Post
        fields = [
            'featured_image',
            'content',
            'status'
        ]
