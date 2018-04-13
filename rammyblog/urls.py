from django.urls import path
from . import views
from accounts import views as account_views

urlpatterns = [
    path('', views.IndexView.as_view(), name ='index'),
    path('tags/<post_tags>/', views.tags, name = 'tags'),
    path('search/', views.search, name = 'search'),
    path('post/<post_slug>/', views.details, name ='details'),
    path('new/post/', views.new_post, name ='new_post'),
    path('post/<post_slug>/edit', views.post_edit, name ='post_edit'),
    path('drafts/', views.post_draft, name ='post_draft'),
    path('post/<post_slug>/publish', views.post_publish, name ='post_publish'),
    path('post/<post_slug>/delete', views.post_delete, name = 'post_delete'),
    path('register', views.register, name = 'register'),
    path('all/drafts', views.admin_draft, name = 'admin_draft'),
    path('profile/@<username>', views.profile, name = 'profile'),
    path('edit-account/', views.accountupdate, name='accountupdate'),
    path('comment/<comment_id>/<post_slug>/edit', views.comment_edit, name = 'comment_edit'),
    path('account_settings', account_views.AccountUpdate.as_view(), name = 'accountsettings'),
    path('comment/<comment_id>/<post_slug>/delete', views.comment_delete, name = 'comment_delete'),
    path('upload/', views.upload_pics, name = 'upload_pics'),
    #path('comment/<pk>/', views.comment_thread, name ='thread'),
   
    
]
