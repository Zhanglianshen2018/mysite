from django.db import models
from django.contrib.auth.models import User


class BlogType(models.Model):
    type_name=models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    blog_type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,verbose_name='博客类型')
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    last_updated_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    isdeleted=models.BooleanField(verbose_name='是否删除')

    def __str__(self):
        return '<Blog : %s>'%self.title




