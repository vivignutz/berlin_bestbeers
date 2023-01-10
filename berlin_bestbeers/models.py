from django.db import models

# Importing USER model
from django.contrib.auth.models import User

#Importing Cloudinary field for geatured image
from cloudinary.models import CloudinaryField

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
    currency_code = models.CharField(max_length=3)  #how to set this with € / €€ / €€€

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
