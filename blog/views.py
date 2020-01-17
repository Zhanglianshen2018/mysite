from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings
from django.db.models import Count

def get_blog_list_common_data(request,blogs_all_list):

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

    #按类型博客数量统计
    #BlogType.objects.annotate(blog_count=Count('blog'))

    #按年月博客数量统计
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict={}

    for blog_date in blog_dates:
        blog_count =Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count

    context = {}

    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    context=get_blog_list_common_data(request,blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_date(request,year,month):

    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    #https://stackoverflow.com/questions/713319/mysql-mysql-tzinfo-to-sql-program/22848483
    context=get_blog_list_common_data(request,blogs_all_list)

    context['blogs_with_date']='%s年%s月' % (year,month)
    #context['blog_dates'] = Blog.objects.dates('created_time', 'month', order="DESC")
    print(context['blog_dates'])
    return render(request, 'blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        blog.readed_time += 1
        blog.save()

    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['last_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog']=blog
    #print("blog %s is read %d times" % (blog.title,blog.readed_time))
    response= render(request, 'blog/blog_detail.html', context) #响应
    response.set_cookie('blog_%s_readed' % blog_pk,'true')
    return response

