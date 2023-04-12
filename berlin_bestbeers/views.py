from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Post, Comment, Bar, Rating, Blog, BarsList
from .forms import CommentForm, PostForm, RatingForm


class HomeView(generic.ListView):
    """
    Displays home page
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


def bar(request, bar_id):
    bar = get_object_or_404(Item, pk=bar_id)
    return render(request, 'bar.html', {'bar': bar})


class Blog(generic.ListView):
    """
    Displays all bars posted
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'
    paginate_by = 12


class Barslist(generic.ListView):
    model = Bar
    template_name = 'bars_list.html'
    ordering = ['-created_on']
    paginate_by = 15


class PostDetail(View):
    """
    Displays a single post
    """

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if (post.status == 0) and (post.author != request.user):
            raise Http404("Post not found.")
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
        if request.user.is_authenticated:
            queryset = Post.objects.filter(status=1)
            post = get_object_or_404(queryset, slug=slug)
            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.name = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
            else:
                comment_form = CommentForm()
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPost(LoginRequiredMixin,
              generic.CreateView):
    """
    To add a post and get a feddback message.
    """
    model = Post
    template_name = 'add_post.html'
    form_class = PostForm
    success_message = 'Post added and waiting for approval!'

    def form_valid(self, form):
        if self.request.POST.get('status'):
            form.instance.status = int(self.request.POST.get('status'))
        form.instance.author = self.request.user
        messages.info(self.request, "Post added and waiting for approval")
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin,
                 generic.UpdateView):
    """
    To update posts
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
        slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': slug})


class PostDelete(LoginRequiredMixin,
                 generic.DeleteView):
    """
    To delete author's own posts
    """
    model = Post
    template_name = 'delete_post.html'
    success_message = 'Post Deleted!'

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
    To like or dislike posts
    """

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentUpdate(LoginRequiredMixin,
                    generic.UpdateView):
    """
    To update own comments in other's posts
    """
    model = Comment
    template_name = 'update_comment.html'
    form_class = CommentForm
    success_message = 'Your comment was successfully updated!'

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentDelete(LoginRequiredMixin,
                    generic.DeleteView):
    """
    To dele won comments on other's posts
    """
    model = Comment
    template_name = 'post_detail.html'
    success_message = 'Comment deleted successfully!'

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('post_detail', kwargs={'slug': slug})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CommentDelete, self).delete(request, *args, **kwargs)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def bar(request, item_id):
    bar = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        bar.rating = rating
        bar.save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'bar.html', {'bar': bar})


def rating(request, bar_id):
    bar = get_object_or_404(Bar, id=bar_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.bar = bar
            rating.user = request.user
            rating.save()
            response = {'success': True}
            return JsonResponse(response)
        else:
            response = {'success': False, 'errors': form.errors}
            return JsonResponse(response)
    else:
        form = RatingForm()
    return render(request, 'rating.html', {'form': form, 'bar': bar})


def rate_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    rating_value = int(request.POST.get('rating'))
    rating = Rating.objects.create(item=item, value=rating_value)
    return JsonResponse({'average_rating': item.average_rating})


def handler404(request, exception):
    """
    Custom 404 page
    """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """
    Custom 500 page
    """
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    """
    Custom 403 page
    """
    return render(request, "errors/403.html", status=403)


def handler405(request, exception):
    """
    Custom 405 page
    """
    return render(request, "errors/405.html", status=405)
