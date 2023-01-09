from django.shortcuts import render
from django.views import generic # immpost django lib
from .models import Post # import post views

#class RecentPostList(generic.ListView):
#    """
#    To display the 3 last posts in created date order
#    """
#    model = Post
#    queryset = Post.objects.filter(status=1).order_by('-created_on')[:3]
#    template_name = 'index.html'

class PostList(generic.ListView):
    """
    This list will display all posts in order by
    date of posting. It will be paginated by 6 blog
    posts on each page
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'
    paginate_by = 6
