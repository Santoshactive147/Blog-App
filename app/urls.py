from django.urls import path,include
from app import views

urlpatterns = [
   
    path('',views.home,name="home"),
    path('add-blog/',views.add_blog,name="add-blog"),
    path('success/',views.success,name="success"),
    path('view/<int:post_id>/', views.view_post, name='view-post'),  # View post
 
]
