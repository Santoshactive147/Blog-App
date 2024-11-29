from django.shortcuts import render

# Create your views here.
from .models import Post,Author,Category
from django.contrib.auth.models import User





def home(request):
    posts = Post.objects.all()

    return render(request,"base.html",{"posts":posts})


from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Author, Category, Post

def add_blog(request):
    if request.method == "POST":
        # Get the form data
        title = request.POST.get('title')
        content = request.POST.get('content')
        author_username = request.POST.get('author')  # Get the author's username from the form
        categories = request.POST.getlist('categories')  # Get the list of categories (assuming multiple categories can be selected)
        is_published = request.POST.get('is_published')  # Get the publication status

        # Convert is_published to a boolean value based on checkbox state
        is_published = is_published == "on"
        
        # Fetch the User object based on the username
        try:
            user = User.objects.get(username=author_username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=author_username, password='default_password123')  # Set a default password or get from request
            print(f"New user {user.username} created!")
        # Check if the Author object exists or create a new one
        author_obj, created = Author.objects.get_or_create(user=user)
        

        # Fetch the Category objects based on the selected category names
        category_objs = []
        for category_name in categories:
            category_obj, created = Category.objects.get_or_create(name=category_name.strip())  # Strip extra spaces
            category_objs.append(category_obj)
        
        # Create the Post object and associate it with the author and categories
        post = Post.objects.create(
            title=title,
            content=content,
            author=author_obj,  # Associate the Author object
            is_published=is_published  # Set the publication status
        )
        
        # Assign the categories to the post using the set() method (for many-to-many field)
        post.categories.set(category_objs)  # Assign categories
        
        print(f"Post created with title: {post.title}, by {author_obj.user.username}")

        # Redirect to a success page or render a confirmation
        return redirect('success')  # Redirect to a success page or any URL you want to display
        
    return render(request, "add_post.html")


def success(request):
    return render(request,"success.html")


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'view_post.html', {'post': post})


