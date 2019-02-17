from django.shortcuts import render_to_response,get_object_or_404,redirect,reverse,render,HttpResponse
from django.http import HttpResponse,JsonResponse
from .models import Article,Article_Kind,UserProfile,About
from django.core.paginator import Paginator
from django.db.models import Count
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
import zhenzismsclient as smsclient
import random,urllib,http,ssl
from random import randint
import qrcode
# Create your views here.
ssl._create_default_https_context = ssl._create_unverified_context
host = ''
sms_send = ''

#博客首页
def index(requset):
    blogs_all_list = Article.objects.all().order_by('-id')
    paginator = Paginator(blogs_all_list,5)
    page_num = requset.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    page_range = list(range(max(currentr_page_num - 2,1),currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2,paginator.num_pages) + 1))
    content = {}
    content['user']= requset.user.username
    content['pages_num'] = paginator.num_pages
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blogs_base_type'] = Article_Kind.objects.annotate(num_posts=Count('article'))
    content['blog_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blogs_page/index.html',content)

#文章详情
def info(request,id):
    content = {}
    blog_info_id= Article.objects.get(id=id)
    content['user'] = request.session.get('user','登录')
    content['blog_info'] = Article.objects.get(id = id)
    content['previous_blog'] = Article.objects.filter(id__lt=blog_info_id.id).last()           #上一篇文章
    content['next_blog'] = Article.objects.filter(id__gt = blog_info_id.id).first()            #下一篇文章
    content['blogs_base_type'] = Article_Kind.objects.annotate(num_posts=Count('article'))
    content['blog_dates'] = Article.objects.dates('created_time', 'month', order='DESC')

    return render_to_response("blogs_page/info.html", content)

#文章分类
def blogs_type(request,id):
    content = {}
    blog_type = get_object_or_404(Article_Kind,id = id)
    blogs_all_list = Article.objects.filter(kind=blog_type).order_by('-created_time')
    paginator = Paginator(blogs_all_list, 5,)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    page_range = list(range(max(currentr_page_num - 5,1),currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2,paginator.num_pages) + 1))
    content['user'] = request.session.get('user','登录')
    content['blogs'] = page_of_blogs
    content['blog_type'] = blog_type
    content['pages_num'] = paginator.num_pages
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blogs_base_type'] = Article_Kind.objects.annotate(num_posts=Count('article'))
    return render_to_response('blogs_page/blogs_type_list.html',content)

#日期归档
def blogs_with_date(request,year,month):
    blogs_all_list = Article.objects.filter(created_time__year=year).order_by('-id')
    paginator = Paginator(blogs_all_list, 5, )
    page_num = request.GET.get('page', 1)  # 获取页码参数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))

    content = {}
    content['user'] = request.session.get('user','登录')
    content['blogs_all_list'] = page_of_blogs
    content['blogs_with_date'] = '%s年' %(year)
    content['pages_num'] = paginator.num_pages
    content['page_of_blogs'] = page_of_blogs
    content['page_range'] = page_range
    content['blog_type'] = Article_Kind.objects.all()
    content['blog_dates'] = Article.objects.dates('created_time', 'month', order='DESC')
    return render_to_response("blogs_page/blogs_with_date.html",content)

#搜索功能--模糊查询
def search(request):
    content = {}
    q = request.GET.get('keyboard')
    if not q:
        content['search_err'] = '你搜索的内容不存在(*╹▽╹*)'
        return render_to_response("blogs_page/search.html", content)
    content['user'] = request.session.get('user','登录')
    post_list = Article.objects.filter(title__contains=q)
    content['post_list'] = post_list
    return render_to_response("blogs_page/search.html",content)

#登录
def login(request):
    content ={}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            usernaem = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request,username=usernaem,password=password)
            if user is not None:
                auth.login(request,user)
                request.session['user'] = user.username
                return redirect(reverse('index'))
            else:
                login_form.add_error(None,'用户名或密码错误')
    else:
        login_form = LoginForm()

    content['login_form'] = login_form
    return render_to_response('blogs_page/login.html',content)
#验证码
def phone_code(requset):
    phone_num = requset.GET.get('telephone')
    client = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com', '100342', 'MGIyNTExYzgtNzUwZS00MjYyLWJkZjgtYWNjZGI2NTk0MzYw')
    code = str(randint(1000,9999))
    result = client.send(phone_num,'欢迎来到TH个人博客，您的验证码是：%s。请不要把验证码泄露给其他人。'%code)
    requset.session['pthon_code'] = int(code)
    return redirect(register)

#注册
def register(request):
    content = {}
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        code = str(request.session.get('pthon_code'))
        telephone_code = request.POST.get('python_code')

        if reg_form.is_valid() and code == telephone_code:
            email = reg_form.cleaned_data['email']
            username = reg_form.cleaned_data['username']
            telephone = reg_form.cleaned_data['telephone']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)
            user_profile = UserProfile(user = user,telephone = telephone)
            user_profile.save()
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('index')))
        else:
            content['yzmcw'] = "验证码错误！"
    else:
         reg_form = RegForm()


    content['reg_form'] = reg_form
    return render_to_response('blogs_page/register.html', content)

#注销
def logout(request):
    auth.logout(request)
    request.session.clear()
    return redirect(reverse('index'))

#about
def about(requset):
    about_info = About.objects.all()
    content = {}
    content['about'] = about_info
    return render_to_response('blogs_page/about.html',content)

import json

def erweima(request):
    content = {}
    if request.method == 'POST':
        text = request.POST.get('text')
        img = qrcode.make(text)
        img.save("./article/static/images/test.png")
    return render_to_response('blogs_page/erweima.html')

from PIL import Image
import ssl,urllib,base64,re
def tupian(request):
    contont = {}
    if request.method == 'POST':
        f1 = request.FILES.get('uploadImage')
        img_typr = str(f1).split('.')[1]
        im_pic = Image.open(f1)
        im_pic.save("./article/static/images/shibie.png")
        host = 'https://wordimg.market.alicloudapi.com'
        path = '/word'
        method = 'POST'
        appcode = 'f7d3602158c1441ca487d36cf4bb8263'
        querys = ''
        bodys = {}
        url = host + path
        with open("./article/static/images/shibie.png", 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
        bodys['image'] = 'data:image/%s;base64,%s'%(img_typr, s)
        post_data = urllib.parse.urlencode(bodys).encode("utf-8")
        request = urllib.request.Request(url, post_data)
        request.add_header('Authorization', 'APPCODE ' + appcode)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(request, context=ctx)
        content = response.read().decode("utf-8")
        txt = re.findall("\"words\"\:\".+?\"", content)
        text = []
        for t in txt:
            if t.startswith('"words":"'):
                s = t.replace('"words":"', "").strip().strip('"')
                text.append(s)
        contont['text'] = ''.join(text)
        return render_to_response('blogs_page/tupianwenzishibie.html',contont)
    return render_to_response('blogs_page/tupianwenzishibie.html')

