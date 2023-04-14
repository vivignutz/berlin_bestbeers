from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


# Create a tuple for our status
STATUS = (
    (0, "Draft"),
    (1, "Published")
)


class Post(models.Model):
    """
    Database model for Posts
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author")
    updated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='post_likes', blank=True)
    instagram_url = models.URLField(
        max_length=200, default='https://www.instagram.com/user', blank=False)
    facebook_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)

    class Meta:
        """
        Posts oder's by date descending
        """
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns a string representation of an object
        """
        return self.title + ' | ' + str(self.author)

    def number_of_likes(self):
        """
        Returns number of blog post likes
        """
        return self.likes.count()

    def get_absolute_url(self):
        """
        Returns successful post to related slug url
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            print(self.slug)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Database model for comments
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
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
        return 'Comment {} by {}'.format(self.body, self.name)


"""
class Bar(models.Model):
    """
# Database model for bar registration
"""
    bar_name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    status = models.IntegerField(choices=STATUS, default=0)
    image = CloudinaryField('image', default='placeholder')
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    created_on = models.DateTimeField(
        auto_now_add=True, default=datetime.datetime.now)

    def __str__(self):
        """
# Returns the name of the bar
"""
        return self.bar_name
"""


class BarsList(models.Model):
    bar_name = models.CharField(max_length=100)
#    address=models.CharField(max_length=400)
    status = models.IntegerField(choices=STATUS, default=0)
    image = CloudinaryField('image', default='placeholder')
#    phone_number=models.CharField(max_length=20)
#    website=models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)

    def __str__(self):
        """
        Returns the name of the bar
        """
        return self.bar_name


class Blog(models.Model):
    """
    Database model for Blog, all posts in one page
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        'auth.User', related_name='blog_likes', blank=True)

    class Meta:
        """
        Posts oder's by date descending
        """
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns a string representation of an object
        """
        return self.title + ' | ' + str(self.author)

    def number_of_likes(self):
        """
        Returns number of blog post likes
        """
        return self.likes.count()

    def get_absolute_url(self):
        """
        Returns successful post to related slug url
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            print(self.slug)
        return super().save(*args, **kwargs)


class Rating(models.Model):
    """
    Database model for rating star
    """
    STAR_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    content = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    rating_stars = models.IntegerField(choices=STAR_CHOICES,
                                       default=0,
                                       validators=[
                                           MinValueValidator(1), MaxValueValidator(5)])
