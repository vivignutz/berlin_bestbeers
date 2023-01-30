from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Post, Comment, PostForm
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
        Post method to comment, save and upload posts.
        User gets a message feedback after posting or uploading.
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

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

class AddPost(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """
    User can add new post and get
    message back
    """
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm
    success_message = 'Post Added!'

    def form_valid(self, form):
        """Validate form after connecting form author to user"""
        if self.request.POST.get('status'):
            form.instance.status = int(self.request.POST.get('status'))
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin,
                SuccessMessageMixin,
                generic.UpdateView,
                PostModelFormView):
    """
    This view allows all users to update their posts
    published or not. A feedback message will be
    displayed when the update is ready.
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
        return reverse_lazy('berlin_bestbeers:home')


#    def update_post(Post,  slug):
#        post = get_object_or_404(post, slug=slug) # id do post
#        form = PostsForm(request.POST or None, request.FILES or None, instance=post) # pega as informações do form

#        if form.is_valid(): # se for valido
#            form.save() # salva

#            messages.warning(request, 'Post updated successfully!')
#            return HttpResponseRedirect(reverse('post_detail', args=[post.slug]))

        # page returns to this template:
#        return render(request, 'post_detail.html', {'form': form})

class PostDelete(LoginRequiredMixin,
                SuccessMessageMixin,
                UserPassesTestMixin,
                generic.DeleteView):
    """
    This view allows users to delete their own blog post
    on the post_detail page. A feedback message will be
    displayed.
    """
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('berlin_bestbeers')
    success_message = 'Post Deleted!'

    def delete(self, request, *args, **kwargs):
        """Generate success message on delete view"""
        messages.success(self.request, self.success_message)
        return super(PostDelete, self).delete(request, *args, **kwargs)

    def test_func(self):
        """Test that logged in user is post author"""
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostLike(LoginRequiredMixin, View):
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


#class Bars(generic.ListView):
    """
    *** This feature will be implemented in the future ***
    This list will display all bars posted by
    the users in form of a list, but only the
    name of the posts without the image.
    """
#    model = Bar
#    queryset = Post.objects.filter(status=1).order_by('-created_on')
#    template_name = 'barlist.html'
#   paginate_by = 12


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
