from django.contrib import admin
from. models import Author,Category,Post
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["user","bio"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","description"]



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title","content","author","get_categories","created_at","updated_at","is_published"]


    def get_categories(self, obj):
        # Return a comma-separated string of category names
           return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'  # Column header in the admin