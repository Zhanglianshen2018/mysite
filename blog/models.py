from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


class BlogType(models.Model):
    type_name=models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title=models.CharField(max_length=50,verbose_name='标题')
    blog_type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,verbose_name='博客类型')
    #content=models.TextField()
    '''
    在模板文件里的content文本前后增加两个标签即可实现，如：
    {% autoescape off %}{{ blog.content}}{% endautoescape %}
    '''
    content = RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    readed_time=models.IntegerField(default=0)
    last_updated_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    isdeleted=models.BooleanField(verbose_name='是否删除',default=False)

    def __str__(self):
        return '<Blog : %s>'%self.title

    class Meta:
        ordering=['-created_time']




