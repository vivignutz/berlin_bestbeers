from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify


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
        User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=25)
    email_contact = models.EmailField(max_length=100)
    opening_hours = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='blogpost_like', blank=True)

    class Meta:
        """
        Posts oder's by date descending
        """
        ordering = ["-created_on"]

    def __str__(self):
        """
        Returns a string representation of an object
        """
        return (self.title + ' | ' + str(self.author) +
                '\nAddress: ' + self.address +
                '\nPhone: ' + self.phone +
                '\nEmail: ' + self.email_contact +
                '\nOpening hours: ' + self.opening_hours)

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


# class Review(models.Model):
    """
    Database model for review
    """
#    title = models.ForeignKey(
#        Post, on_delete=models.CASCADE, related_name="review")
#    author = models.ForeignKey(User, on_delete=models.CASCADE)
#    rating = models.IntegerField(choices=STAR_CHOICES)
#    created_on = models.DateTimeField(auto_now_add=True)

#    class Meta:
#        ordering = ['-created_on']

#    def __str__(self):
#        return f'{self.author} - {self.post.title}'


class Review(models.Model):
    tittle = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.tittle
