from django.contrib import admin
from .models import BlogType,Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

    def __str__(self):
        return self.type_name

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','blog_type','readed_time','author','created_time','last_updated_time')

    def __str__(self):
        return '<Blog : %s>'%self.title
