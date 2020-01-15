from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings



def blog_list(request):

    blogs_all_list=Blog.objects.all()
    paginator=Paginator(blogs_all_list,settings.BLOG_NUMBER_EACH_PAGE) #每10页进行分页，Iaravel分页极为简单;为了测试每页显示2张
    page_num = request.GET.get('page', 1)  # 获取url页码参数（GET请求）获取当前点击页页码，如果没有点击，则默认是第一页
    #print("页码是"+str(page_num))
    page_of_blogs=paginator.get_page(page_num)
    current_page=page_of_blogs.number#获取当前页码
    page_range = [(current_page + i) for i in range(-3, 3) if paginator.num_pages >= (current_page + i) > 0]

    #加上前后省略号
    if page_range[0]-1>=2:
        page_range.insert(0,"...")
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append("...")

    #加上首页，尾页
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['page_of_blogs']=page_of_blogs
    context['blog_types']=BlogType.objects.all()
    context['page_range']=page_range
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render(request, 'blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):

    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)


    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, settings.BLOG_NUMBER_EACH_PAGE)  # 每10页进行分页，Iaravel分页极为简单;为了测试每页显示2张
    page_num = request.GET.get('page', 1)  # 获取url页码参数（GET请求）获取当前点击页页码，如果没有点击，则默认是第一页
    # print("页码是"+str(page_num))
    page_of_blogs = paginator.get_page(page_num)
    current_page = page_of_blogs.number  # 获取当前页码
    page_range = [(current_page + i) for i in range(-3, 3) if paginator.num_pages >= (current_page + i) > 0]

    # 加上前后省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")

    # 加上首页，尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    context['page_range'] = page_range
    return render(request, 'blog/blogs_with_type.html', context)
