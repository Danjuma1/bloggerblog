from django.contrib import admin
from .models import Blogpost, Comment, UserProfile
from markdownx.admin import MarkdownxModelAdmin 
class BlogpostAdmin(admin.ModelAdmin):
         list_display = (
        'title',
        'slug',
        'author',
        'pub_date',
        'updated',
        
    )
         list_filter = ('author', 'pub_date', 'created_date')
         search_fields = ('title', 'content')
         date_hierarchy = 'pub_date'
         raw_id_fields = ('author',)
         ordering = ['created_date', 'pub_date', 'updated']
class CommentAdmin(admin.ModelAdmin):
     list_display = (
        'message',
        'topic',
        'created_at',
        'created_by',
        'active',
    )
     list_filter = (  
        'topic',
        'created_at',
        'created_by',
        'active',)
     search_fields = (  'topic', 'message')


class UserAdmin(admin.ModelAdmin):
     list_display = (
        'user',
        'website',
        'city',
        'phone',
    )
     list_filter = (  
        'user',
        'website',
        'city',
        'phone',)
     search_fields = (  'user', 'city', 'phone',)
     
"""class Taggit(admin.ModelAdmin):
    list_display = ['tag_list',]

    def get_queryset(self, request):
        return super(Taggit, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
"""
admin.site.register(Blogpost, BlogpostAdmin,)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserAdmin)
#admin.site.register(Taggit )

# Register your models here.
