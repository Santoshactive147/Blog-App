from django.shortcuts import render

# Create your views here.
from .models import Post,Author,Category
from django.contrib.auth.models import User




from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        return render(request, "base.html", {"posts": posts})
    else:
        # If not authenticated, you can redirect to the login page or any other page
        return redirect('login')  # Redirects to login page

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Author, Category, Post

def add_blog(request):
    if request.method == "POST":
      
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_username = request.POST.get('author') 
        categories = request.POST.getlist('categories')  
        is_published = request.POST.get('is_published')  

       
        is_published = is_published == "on"
        
     
        try:
            user = User.objects.get(username=author_username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=author_username, password='default_password123')  # Set a default password or get from request
            print(f"New user {user.username} created!")
       
        author_obj, created = Author.objects.get_or_create(user=user)
        

       
        category_objs = []
        for category_name in categories:
            category_obj, created = Category.objects.get_or_create(name=category_name.strip())  # Strip extra spaces
            category_objs.append(category_obj)
        
       
        post = Post.objects.create(
            title=title,
            content=content,
            author=author_obj, 
            is_published=is_published  
        
        )
        post.categories.set(category_objs)  
        
        print(f"Post created with title: {post.title}, by {author_obj.user.username}")

        
        return redirect('success')  
        
    return render(request, "add_post.html")


def success(request):
    return render(request,"success.html")


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_post.html', {'post': post})


def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)

    post.delete()
    return redirect('home') 


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, Author, Category
from django.contrib.auth.models import User

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_username = request.POST.get('author')
        categories = request.POST.getlist('categories')  # Retrieve category IDs
        is_published = request.POST.get('is_published') == 'on'

        # Fetch the User instance by username
        try:
            user = User.objects.get(username=author_username)
        except User.DoesNotExist:
            return render(request, 'edit_post.html', {
                'post': post,
                'categories': Category.objects.all(),
                'error_message': f"User '{author_username}' does not exist."
            })

        # Fetch the Author instance linked to the user
        try:
            author = Author.objects.get(user=user)
        except Author.DoesNotExist:
            return render(request, 'edit_post.html', {
                'post': post,
                'categories': Category.objects.all(),
                'error_message': f"Author profile for user '{author_username}' does not exist."
            })

        # Update the post object
        post.title = title
        post.content = content
        post.author = author  # Assign the Author instance
        post.is_published = is_published

        # Set the categories by retrieving the corresponding Category instances
        post.categories.set(Category.objects.filter(id__in=categories))  # Use category IDs to get the categories

        post.save()
        messages.success(request, "The blog post has been updated successfully.")
        return redirect('view-post', post_id=post.id)

    # Pass all categories to the template for the form
    categories = Category.objects.all()
    return render(request, 'edit_post.html', {'post': post, 'categories': categories})



# views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home') 




# views.py
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:    
           print(form.errors)    
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
