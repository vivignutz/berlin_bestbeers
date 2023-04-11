from django import forms
from .models import Post, Comment, Review


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
    (1, '1 estrela'),
    (2, '2 estrelas'),
    (3, '3 estrelas'),
    (4, '4 estrelas'),
    (5, '5 estrelas'),
)


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(
        choices=STAR_CHOICES, widget=forms.RadioSelect())
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
