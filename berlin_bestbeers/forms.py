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


STAR_CHOICES = (
    (1, '1 star'),
    (2, '2 stars'),
    (3, '3 stars'),
    (4, '4 stars'),
    (5, '5 stars'),
)


class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        choices=STAR_CHOICES, widget=forms.RadioSelect())
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
