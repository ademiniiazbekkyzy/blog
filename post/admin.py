from django.contrib import admin

# Register your models here.
from post.models import Image, Post, Rating, Category

admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Image)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]