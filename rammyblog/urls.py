from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('post/<post_id>/', views.details, name ='details'),
    path('new/post/', views.new_post, name ='new_post'),
    path('post/<post_id>/edit', views.post_edit, name ='post_edit'),
    path('drafts/', views.post_draft, name ='post_draft'),
    path('post/<post_id>/publish', views.post_publish, name ='post_publish'),
    path('post/<post_id>/delete', views.post_delete, name = 'post_delete'),
    path('register', views.register, name = 'register'),
    path('all/drafts', views.admin_draft, name = 'admin_draft')


]
