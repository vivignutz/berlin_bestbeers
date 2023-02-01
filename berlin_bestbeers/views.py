from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import CommentForm, PostForm


class HomeView(generic.ListView):
    """
    This view will display the home page with the
    banner and 6 bars posted in order by date of posting.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class BarList(generic.ListView):
    """
    This viwe will display a list of all bars/posts
    posted by the users and approved by the admin.
    This view doesn't show the banner.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'barlist.html'
    paginate_by = 12


class PostDetail(View):
    """
    View of each single post on a single page. Comment
    and/or like can be included by the user as well.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Get method: to recover post details including
        comments and likes to render post detail page.
        """
        post = get_object_or_404(Post, slug=slug)
        if (post.status == 0) and (post.author != request.user):
            raise Http404("Post not found.")
        #queryset = post.comments.filter(status=1)
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
        Post method to comment, save and upload posts. User
        gets a message feedback after posting or uploading.
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
                messages.success(request, 'Comment added')
            else:
                comment_form = CommentForm()
        """
        Returns to the post detail page
        """
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPost(LoginRequiredMixin,
            generic.CreateView):
    """
    User adds a new post and gets a feddback message.
    """
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm
    success_message = 'Post Added!'

    def form_valid(self, form):
        """
        Validated form after connecting author to user.
        """
        if self.request.POST.get('status'):
            form.instance.status = int(self.request.POST.get('status'))
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,
                generic.UpdateView):
    """
    This view allows all users to update their own
    posts, published or not. A feedback message will
    be displayed when the update is ready.
    """
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'
    success_message = 'Post updated successfully!'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))

    def form_valid(self, form):
        super(PostUpdate, self).form_valid(form)
        self.object = self.get_object()
        if self.request.user == self.object.author:
            form = form.save(commit=False)
            form.save()
            messages.info(self.request, "Post Updated")
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, "You can't update this post!")
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('home')


class PostDelete(LoginRequiredMixin,
                generic.DeleteView):
    """
    This view allows users to delete their own blog posts
    while logged in. A feedback message will be displayed.
    """
    model = Post
    template_name = 'delete_post.html'
    success_message = 'Post Deleted!'
#    context_object_name = 'project'

    def get_object(self):
        return get_object_or_404(Post, slug=self.kwargs.get('slug'))

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object.author:
            self.object.delete()
            messages.info(self.request, "Post Deleted!")
        else:
            messages.error(self.request, "You can't delete this post!")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('home')


class PostLike(View):
    """
    View is to like or remove likes on posts.
    """
    def post(self, request, slug, *args, **kwargs):
        """
        Post method to toggle post like and
        redirect to the post detail page.
        """
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentUpdate(LoginRequiredMixin,
                    generic.UpdateView):
    """
    View to allow users to update their comment
    on the post detail page
    Success message as user feedback
    """
    model = Comment
    template_name = 'comment_update.html'
    form_class = CommentForm
    success_message = 'Comment updated successfully!'

    def get_success_url(self):
        """Success url for post associated with comment"""
        slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': slug})

    def form_valid(self, form):
        """Validate form after connecting form author to user"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Test that logged in user is comment author"""
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentDelete(LoginRequiredMixin,
                    generic.DeleteView):
    """
    View to allow users to delete their comment
    on the post detail page
    Success message as user feedback
    """
    model = Comment
    template_name = 'post_detail.html'
    success_message = 'Comment deleted successfully!'

    def get_success_url(self):
        """Success url for post associated with comment"""
        slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': slug})

    def delete(self, request, *args, **kwargs):
        """Generate success message on delete viev"""
        messages.success(self.request, self.success_message)
        return super(CommentDelete, self).delete(request, *args, **kwargs)

    def test_func(self):
        """Test that logged in user is comment author"""
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


"""
This is a feature to be implemented in the future. It'll
display all bars posts in form of a list without the image.
"""
"""
class Bars(generic.ListView):
    model = Bar
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'barlist.html'
    paginate_by = 12

    def handler404(request, exception):
        return render(request, '404.html', status=404)


    def handler500(request):
        return render(request, '500.html', status=500)
"""
