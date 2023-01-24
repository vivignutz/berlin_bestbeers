from django.contrib import admin
from .models import Post, Comment, Bar
from django_summernote.admin import SummernoteModelAdmin
#from crispy import berlin_bestbeers


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Post model for admin pannel
    """
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Comment model for admin pannel.
    All comments have to be reviewed by admin
    """
    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    list_filter = ('approved', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        """
        Approve user comments method
        """
        queryset.update(approved=True)

# This feature of Bar list with addresses
# like a guide will be implemented in
# a near future.
#admin.site.register(Bar)