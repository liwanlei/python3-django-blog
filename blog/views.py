# -*- coding:utf-8 -*-  
from django.shortcuts import render,redirect
from blog.models import *
from django.http import Http404, HttpResponseRedirect,HttpResponse
from  django.db import  connection
from  django.db.models import  Count
from django.conf import  settings
from blog.create_yanzheng import generate_verification_code
from blog.send_email import send_text
from blog.times_puls import time_plus
from datetime import  datetime as  dates
from django import forms
import os,time,re
from PIL import Image
from blog.fenye import fenye
from django.contrib.auth.decorators import login_required
from blog.pipei_user import *
import datetime
from datetime import datetime, timedelta
def global_setting(request):
    Tag_list = Tag.objects.all()
    post1 = Article.objects.all()
    click_count= Article.objects.values('click_count').order_by('-click_count')
    read_list=(Article.objects.get(click_count=click['click_count'])for click in (click_count[:5]))
    coment_count_list = Comment.objects.values('article').annotate(coment_count=Count("article")).order_by(
        '-coment_count')
    beijing_post_list = (Article.objects.get(pk=coment_count['article']) for coment_count in (coment_count_list[:5]))
    teing_list=Links.objects.all()
    fenlei_list = Catagory.objects.all()
    if 'username' in request.session:
        username = request.session['username']
        me = Article.objects.filter(users__exact=(User.objects.filter(username__exact=username)))
        h=0
        for i in me:
            comu = (Comment.objects.filter(user__comment__article=i).filter(date_publish__gte=(User.objects.get(username__exact=username)).last_login).filter(date_publish__lte=dates.utcnow())).count()
            h+=int(comu)
        if h==0:
            return {'Tag_list': Tag_list, 'post_list': read_list, 'post_list_ping': beijing_post_list,'chaolianjie': teing_list, 'username': username}
        return {'Tag_list':Tag_list,'post_list':read_list,'post_list_ping':beijing_post_list,'chaolianjie':teing_list,'username':username,'coumn':h}
    else:
        return {'Tag_list':Tag_list,'post_list':read_list,'post_list_ping':beijing_post_list,'chaolianjie':teing_list}
def home(request):
    posts = Article.objects.all()
    count=[]
    for post in posts:
        count.append((Comment.objects.filter(comment__article=post)).count())
    post_list = fenye(request, posts=posts)
    return render(request,'index.html',{'post_list':post_list,'count':count})
def python(request):
    posts=Article.objects.filter(tag__name='python')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def ceshi(request):
    posts=Article.objects.filter(tag__name=u'测试')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def qianduan(request):
    posts=Article.objects.filter(tag__name=u'前端')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def appium(request):
    posts=Article.objects.filter(tag__name='appium')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def selenium(request):
    posts=Article.objects.filter(tag__name='selenium')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def git(request): #git 文章获取
    posts=Article.objects.filter(tag__name=u'git')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def Mysql(request): #Mysql 文章获取
    posts=Article.objects.filter(tag__name='MySQL')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def guanli(request): #管理 文章获取
    posts=Article.objects.filter(tag__name=u'管理')
    post_list = fenye(request, posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def dashuju(request): #大数据 文章获取
    posts=Article.objects.filter(tag__name=u'大数据')
    post_list=fenye(request,posts=posts)
    return render(request, 'index.html', {'post_list': post_list,})
def login(request):
    errors_list = []
    if request.method == 'GET':
        # 记住来源的url，如果没有则设置为首页('/')
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    elif request.method == 'POST':
        if request.method == 'GET':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        elif request.method == 'POST':
            username=request.POST.get('username',None)
            password=request.POST.get('password',None)
            user = User.objects.filter(username__exact = username,password__exact = password)
            request.session['username'] = username
            if user:
                if request.session['login_from']=='http://127.0.0.1:8000/reg' or request.session['login_from']=='http://127.0.0.1:8000/xiugaimima':
                    response=HttpResponseRedirect('/')
                    response.set_cookie('username', username, 3600)
                    return response
                response= HttpResponseRedirect(request.session['login_from'])
                response.set_cookie('username', username, 3600)
                return response
            return render(request,'login.html',{'msg':'用户名或者密码错误'})
    return render(request,'login.html')
def reg(request):
    if request.method=='POST':
        username=request.POST['username']
        if len(getuser(username))<=0:
            return render(request,'reg.html',{'msg':u'用户名应该是6-16组成'})
        passwor1 = request.POST['password']
        passwor2 = request.POST['password1']
        shouj = request.POST['shouji']
        if len(getPhoneNumFromFile(shouj))<=0:
            return render(request, 'reg.html', {'msg':u'手机号格式是否正确'})
        shouji = User.objects.filter(mobile__exact=shouj)
        if shouji:
            return render(request, 'reg.html', {'msg': u'手机号已经存在'})
        youjian = request.POST['email']
        if len(getMailAddFromFile(youjian))<=0:
            return render(request, 'reg.html', {'msg': u'邮箱格式是否正确'})
        use=User.objects.filter(username__exact=username)
        if use:
            return render(request,'reg.html',{'msg':u'用户名已经存在'})
        else:
            if passwor1==passwor2:
                use1=User()
                use1.username=username
                use1.password=passwor1
                use1.mobile=shouj
                use1.email=youjian
                use1.save()
                return HttpResponseRedirect('login')
            else:
                return render(request,'reg.html',{'msg':u'请查看密码是否一致'})
    return render(request,'reg.html')
def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        p1=Article.objects.get(id=str(id))
        p1.click_count+=1
        p1.save()
        commn__list = Comment.objects.filter(article__title=post)
        if request.method=='POST':
            username = request.session['username']
            if username:
                content=request.POST['content']
                if len(content)>0:
                    article=Article.objects.get(id=str(id))
                    user=User.objects.get(username=username)
                    con=Comment()
                    con.article=article
                    con.content=content
                    con.user=user
                    con.save()
                    return render(request, 'post.html', {'post': post, 'commn__list': commn__list})
                else:
                    return render(request,'post.html',{'msg':u'评论不能为空'})
            return render(request, 'post.html', {'msg': u'请登陆后评论'})
        else:
            return render(request, 'post.html', {'post': post,'commn__list':commn__list})
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post, 'commn__list': commn__list})
def logout(request):
   # request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    try:
        user = User.objects.get(username__exact=request.session['username'])
        user.last_login= datetime.utcnow()
        user.save()
        del request.session['username']
        return render(request,'index.html')
    except:
        return HttpResponseRedirect('/')
def gerenzhongxin(request):
    try:
        username = request.session['username']
        try:
            post_list6 = Article.objects.filter(users__username=username)
            post_list = fenye(request, posts=post_list6)
            readlist = post_list6.order_by('-click_count')[0:6]
            me = Article.objects.filter(is_recommend=True)
            tuijian_list = me.filter(users__username=username)
            me = Article.objects.filter(users__exact=(User.objects.filter(username__exact=username)))
            comu=[]
            for i in me:
                comu.extend(Comment.objects.filter(user__comment__article=i).filter(date_publish__gte=(User.objects.get(username__exact=username)).last_login))
            if len(comu)<=0:
                return render(request, 'gerenzhongxin.html',{"post_list": post_list, 'readlist': readlist, 'tuijian_list': tuijian_list})
            return render(request, 'gerenzhongxin.html',{"post_list": post_list, 'readlist': readlist, 'tuijian_list': tuijian_list,"comu_list":comu})
        except:
            return render(request, 'gerenzhongxin.html',)
    except:
        return redirect('/')
def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'index.html')
        else:
            post_list = Article.objects.filter(title__contains=s)
            if len(post_list) == 0 :
                return render(request,'archives.html', {'post_list' : post_list,
                                                    'error' : True})
            else :
                return render(request,'archives.html', {'post_list' : post_list,
                                                        'error' : False})
    return redirect('/')
def reset_pwd(request):
    if request.method=='POST':
        user= request.POST['firstname']
        email=request.POST['email']
        use=User.objects.filter(username__exact=user)
        emai=User.objects.filter(email__exact=email)
        if use:
            if emai:
                user_ex = User_ex.objects.filter(email=email)
                if len(user_ex)>0:
                    user_ex=user_ex[0]
                    create_time = user_ex.valid_time
                    datime_now=dates.now()
                    ts=time_plus(datime_now,create_time)
                    if ts<60:
                        return render(request,'zhaohui.html',{'msg':'60秒内只能找回一次'})
                    try:
                        user_ex.delete()
                        code = generate_verification_code(10)
                        to_addr = email
                        email = email
                        code = code
                        s = send_text(to_addr=to_addr, email=email, code=code)
                        if s == 200:
                            User_ex.objects.create(email=email, valid_code=code)
                            return render(request,'chongzhi.html')
                        else:
                            return render(request, 'zhaohui.html', {'msg': '找回失败，请联系管理员，或者重新找回'})
                    except:
                        code=generate_verification_code(10)
                        to_addr=email
                        email=email
                        code=code
                        s=send_text(to_addr=to_addr,email=email,code=code)
                        if s==200:
                            User_ex.objects.create(email=email,valid_code=code)
                            return HttpResponseRedirect('chongzhi.html')
                        else:
                            return render(request,'zhaohui.html',{'msg':'找回失败，请联系管理员，或者重新找回'})
                code = generate_verification_code(10)
                to_addr = email
                email = email
                code = code
                s = send_text(to_addr=to_addr, email=email, code=code)
                if s == 200:
                    User_ex.objects.create(email=email, valid_code=code)
                    return render(request,'chongzhi.html')
                else:
                    return render(request, 'zhaohui.html', {'msg': '找回失败，请联系管理员，或者重新找回'})
            else:
                return render(request, 'zhaohui.html',{'msg':'邮箱不存在'})
        else:
            return render(request, 'zhaohui.html', {'msg': '用户名不存在'})
    return render(request,'zhaohui.html')
def ret_passord(request):
    if request.method=='POST':
        email=request.POST['email']
        yanzhengma = request.POST['yanzhengma']
        inputPassword = request.POST['inputPassword']
        inputPassword1 = request.POST['inputPassword1']
        email1=User_ex.objects.filter(email=email)
        if email1:
            emaile=email1[0]
            email_date=emaile.valid_time
            time_plu=dates.now()
            td=time_plus(time_plu,email_date)
            if td>=600:
                return render(request, 'chongzhi.html',{'msg':'验证码超过有效期'})
            else:
                if yanzhengma == emaile.valid_code:
                    if inputPassword==inputPassword1:
                        if inputPassword==User.objects.get(email=email).password:
                            return render(request, 'chongzhi.html', {'msg': '密码与最近修改一致'})
                        me = User.objects.get(email=email)
                        me.password = inputPassword
                        me.save()
                        User_ex.objects.filter(email=email).delete()
                        return HttpResponseRedirect('login.html')
                    return render(request, 'chongzhi.html', {'msg': '请确认密码'})
                return render(request, 'chongzhi.html', {'msg': '验证码有误'})
        else:
            return render(request, 'chongzhi.html', {'msg': '邮箱不存在'})
    return render(request,'chongzhi.html')
def xiugaimima(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login')
    username = request.session['username']
    if request.method=='POST':
        password=request.POST['pass_yuan']
        xiu_pass=request.POST['inputPassword']
        que_pass = request.POST['inputPassword1']
        pass1=User.objects.get(username=username).password
        if pass1==password:
            if xiu_pass==que_pass and len(getuser(xiu_pass))>0 and xiu_pass!=password:
                usern=User.objects.get(username=username)
                usern.password=xiu_pass
                usern.save()
                return redirect('login.html')
            return render(request, 'xiugai.html',{'msg':'请确认修改密码'})
        return render(request, 'xiugai.html', {'msg': '原密码输入有误'})
    return render(request, 'xiugai.html')
def xiebo(request):
    if  not request.session.get('username'):
        return  HttpResponseRedirect('login')
    username = request.session['username']
    fen1=Catagory.objects.all()
    if request.method=='POST':
        user=User.objects.get(username=username)
        title=request.POST['biaoti1']
        try:
            titl=Article.objects.get(title=title)
            return render(request, 'xiebo.html', {'msg': "文章标题不能重复",'fenlei_list':fen1})
        except:
                if len(title)<=0:
                    return render(request,'xiebo.html',{'msg':"标题不能为空",'fenlei_list':fen1})
                content=request.POST['content']
                fenle=request.POST['jumpMenu']
                fen=Catagory.objects.get(name=fenle)
                if len(fenle)<=0:
                    return render(request, 'xiebo.html', {'msg': "标签不能为空",'fenlei_list':fen1})
                biaoqian_list= request.POST.getlist('checkbox')
                biaoqian=(Tag.objects.get(name=biaoqian)for biaoqian in biaoqian_list)
                try:
                    tuijian=request.POST['tuijian']
                    tuijian=True
                except:
                    tuijian=False
                bei=Article()
                bei.users=user
                bei.title=title
                bei.categorys=fen
                bei.content=content
                bei.desc=content[:10]
                bei.is_recommend=tuijian
                for i in biaoqian:
                    bei.tag.add(i)
                bei.save()
                return redirect('geren')
    return render(request,'xiebo.html',{'fenlei_list':fen1})
def zhongxin(request,id):
    user=User.objects.get(id=str(id))
    post_list=Article.objects.filter(users__username=user)
    readlist=post_list.order_by('-click_count')[0:5]
    me=Article.objects.filter(is_recommend=True)
    tuijian_list=me.filter(users__username=user)
    return render(request,'geren.html',{'user':user,"post_list":post_list,'readlist':readlist,'tuijian_list':tuijian_list})
def shangchuantouxiang(request):
    try:
        username = request.session['username']
        if request.method=='POST':
            photo = request.FILES['touxiang']

            photo_last = str(photo).split('.')[-1]
            photoname = '%s.%s' % (username, photo_last)
            img = Image.open(photo)
            img.save('touxiang/' + photoname)
            try:
                be=User.objects.get(username__exact=username)
                be.avatar=photoname
            except Exception as e:
                print(e)
            return redirect('gerenzhongxin.html')
        return render(request,'xiu_touxiang.html')
    except:
        return  redirect('login.html')
def bianji(request,id):
    if  not request.session.get('username'):
        return  redirect('login')
    post_user=Article.objects.get(id=id)
    fenlei=Catagory.objects.all()
    user=User.objects.get(username=request.session.get('username'))
    if post_user.users_id==user.id:
        if request.method =='POST':
            title=request.POST['biaoti1']
            if len(title) <= 0:
                return render(request, 'xiebo.html', {'msg': "标题不能为空", 'fenlei_list': fenlei})
            content = request.POST['content']
            fenle = request.POST['jumpMenu']
            fen = Catagory.objects.get(name=fenle)
            if len(fenle) <= 0:
                return render(request, 'xiebo.html', {'msg': "标签不能为空", 'fenlei_list': fenlei})
            biaoqian_list = request.POST.getlist('checkbox')
            biaoqian = (Tag.objects.get(name=biaoqian) for biaoqian in biaoqian_list)
            try:
                tuijian = request.POST['tuijian']
                tuijian = True
            except:
                tuijian = False
            post_user.title=title
            post_user.categorys=fen
            post_user.content = content
            post_user.desc=content[:10]
            post_user.is_recommend = tuijian
            post_user.click_count=post_user.click_count
            for i in biaoqian:
                post_user.tag.add(i)
            post_user.save()
            return  redirect('home')
        return  render(request,'edit.html',{'post':post_user,'fenlei_list':fenlei})
    return redirect('xiebo')
