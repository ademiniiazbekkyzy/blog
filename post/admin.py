from django.contrib import admin

# Register your models here.
from post.models import Image, Post, Rating, Category, Favorite, Comments

admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Image)
admin.site.register(Favorite)
admin.site.register(Comments)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
