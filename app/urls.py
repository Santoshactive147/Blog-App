from django.urls import path,include
from app import views
from .views import CustomLoginView
from django.contrib.auth.views import LoginView, LogoutView 
urlpatterns = [
   
    path('home/',views.home,name="home"),
    path('add-blog/',views.add_blog,name="add-blog"),
    path('success/',views.success,name="success"),
    path('view/<int:post_id>/', views.view_post, name='view-post'), 
    path('delete-post/<int:post_id>/',views.delete_post,name="delete-post"),
    path('edit-post/<int:post_id>/',views.edit_post,name="edit-post"),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

  
 
]



