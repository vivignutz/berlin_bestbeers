from django import forms
from .models import Post, Comment, Rating


class CommentForm(forms.ModelForm):
    """
    Form for comments
    """
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        """
        Remove body label and add placeholder text
        """
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = ''
        self.fields['body'].widget.attrs['placeholder'] = 'Add a comment here:'


class PostForm(forms.ModelForm):
    """
    Form for posts
    """
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'excerpt',
            'featured_image',
        ]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating',]
        widgets = {
            # 'rating': forms.Select(choices=Rating.STAR_CHOICES)
            'rating': forms.HiddenInput()
        }
