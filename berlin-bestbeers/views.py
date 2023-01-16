from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View # immport django View from django
from django.http import HttpResponseRedirect
from django.contrib import messages #import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Post, Comment #import post views and comments
from .forms import CommentForm, PostForm


class PostList(generic.ListView):
    """
    This list will display all posts in order by
    date of posting. It will be paginated by 6 blog
    posts on each page
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6

class PostDetail(View):
    """
    View of each posts on a single blog page.
    Comment and/or like can be included as well.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Used GET method to recover post details including
        comments and likes and render post detail page
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Use POST methode to comment, save and upload post.
        User gets a message of the post success
        """
        if request.user.is_authenticated:
            queryset = Post.objects.filter(status=1)
            post = get_object_or_404(queryset, slug=slug)
            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, 'Comment Added')

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class PostLike(LoginRequiredMixin, View):
    """
    This view is to like or remove like on post
    """
    def post(self, request, slug, *args, **kwargs):
        """
        Post method to toggle post like and redirect
        to post detail page
        """
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class PostAdd(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    User can add new post and get
    message back
    """
    model = Post
    template_name = 'post_add.html'
    form_class = PostForm
    success_message = 'Post Added'

    def form_valid(self, form):
        """Validate form after connecting form author to user"""
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    """
    User can update their posts
    and get the message tha it was successfull.
    """
    model = Post
    template_name = 'post_update.html'
    form_class = PostForm
    success_message = 'Post Updated'

    def form_valid(self, form):
        """Validate form after connecting form author to user"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Test that logged in user is post author"""
        post = self.get_object()
        if self.request.user == post.author:
            return True
            return False


def handler404(request, exception):
    """
    Custom 404 page
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    Custom 500 page
    """
    return render(request, '500.html', status=500)