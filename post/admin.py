from django.contrib import admin

# Register your models here.
from post.models import Image, Post


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]