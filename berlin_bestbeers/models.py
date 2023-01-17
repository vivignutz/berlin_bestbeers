from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
#from django.template.defaultfilters import slugify

"""
# Create a tuple for user gender choice
GENDER_CHOICES = (
    ('m', 'Masculin'),
    ('f', 'Feminin'),
    ('d', 'Divers')
)

class User(models.Model):
    name = models.CharField(max_length=30)
    birthday = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
"""

# Create a tuple for our status
STATUS = ((0, "Draft"), (1, "Published"))

class Post(models.Model):
    """
    Database model for Posts
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)

    class Meta:
        """
        Set the order of posts by date descending
        """
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns a string representation of an object
        """
        return self.title

    def number_of_likes(self):
        """
        Returns number of blog post likes
        """
        return self.likes.count()


class Comment(models.Model):
    """
    Database model for comments
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        """
        The order of comments by date ascending order
        """
        ordering = ['created_on']

    def __str__(self):
        """
        Returns comment with body and name
        """
        return f'Comment {self.body} by {self.author}'

class Bar(models.Model):
    """
    Database model for bar registration
    """
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.bar


class BarReview(models.Model):
    """
    Database model for bar review
    """
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=600)
    created_on = models.DateTimeField()

    # To ensure that only admins can make bar reviews
    # to avoid double insertions of bar names
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bar

