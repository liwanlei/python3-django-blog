# -*- coding:utf-8 -*-  
import redis
from datetime import datetime
from datetime import datetime as  dates
from django.views.decorators.cache import cache_page
from public.fenye import fenye
from public.pipei_user import *
from public.times_puls import time_plus
from  django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect,render_to_response,RequestContext
from django.views.generic.base import View
from blog.models import *
from django.views.decorators.csrf import csrf_protect
from public.create_yanzheng import generate_verification_code
from public.send_email import send_text
from django.contrib.auth.hashers import make_password, check_password
r=redis.Redis(host='127.0.0.1',port=6379,db=0)
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
    return {'Tag_list':Tag_list,'post_list':read_list,'post_list_ping':beijing_post_list,'chaolianjie':teing_list}
class HomeView(View):
    def get(self,request):
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
@cache_page(60*15)
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

class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        next = request.META.get('HTTP_REFERER')
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        try:
            user = User.objects.get(username= username)
            if user.is_login==True:
                return render_to_response(request, 'login.html',{'msg': '同时只能登陆一台设备!'})
            if user.login_sta==True:
                return render_to_response(request, 'login.html', {'msg': '账号已经冻结!'})
            if (datetime.datetime.now()-user.login_suo).total_seconds() <600:
                return render_to_response(request, 'login.html', {'msg': '账号锁定十分钟内不能登陆!'})
            if user.pass_errnum>5:
                user.login_suo=datetime.datetime.now()
                return render_to_response(request, 'login.html', {'msg': '密码输入超过5次，用户锁定十分钟'})
            if check_password(password,user.password) :
                request.session['username'] = username
                if '/logout' or '/reg' in next:
                    response = HttpResponseRedirect('/')
                else:
                    response= HttpResponseRedirect(next)
                user.last_login=datetime.datetime.now()
                user.is_login=True
                user.pass_errnum=0
                user.save()
                response.set_cookie('username', username, 3600)
                return response
            user.pass_errnum+=1
            user.save()
            return render_to_response(request, 'login.html', {'msg': '密码错误'})
        except:
            return render_to_response(request,'login.html',{'msg':'用户名不存在！'})
class RegView(View):
    def get(self,request):
        return  render(request,'reg.html')
    def post(self,request):
        ipreques = request.META['REMOTE_ADDR']
        ip_re = r.get(ipreques)
        if ip_re:
            return render(request, 'reg.html', {'msg': u'10分钟只能注册一次'})
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
                use1.password=make_password(passwor1)
                use1.mobile=shouj
                use1.email=youjian
                use1.save()
                r.set(ipreques,1,ex=600)
                return HttpResponseRedirect('login')
            else:
                return render(request,'reg.html',{'msg':u'请查看密码是否一致'})
class DetailView(View):
    def get(self,request,id):
        post = Article.objects.get(id=str(id))
        p1 = Article.objects.get(id=str(id))
        p1.click_count += 1
        p1.save()
        commn__list = Comment.objects.filter(article__title=post)
        return render(request, 'post.html', {'post': post, 'commn__list': commn__list})
    def post(self,request, id):
        try:
            post = Article.objects.get(id=str(id))
            commn__list = Comment.objects.filter(article__title=post)
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
                return render(request,'post.html',{'msg':u'评论不能为空'})
            return render(request, 'post.html', {'msg': u'请登陆后评论'})
        except Article.DoesNotExist:
            raise Http404
class LogoutView(View):
    def get(self,request):
        try:
            user = User.objects.get(username__exact=request.session['username'])
            user.last_login=datetime.datetime.now()
            user.is_login=False
            user.save()
            del request.session['username']
            return render(request,'index.html')
        except:
            return HttpResponseRedirect('/')
class GerenzhongxinView(View):
    def get(self,request):
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
class BlogSearchView(View):
    def get(self,request):
        return render(request, 'archives.html',{})
    def post(self,request):
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
class ResetpwdView(View):
    def get(self,request):
        return render(request, 'zhaohui.html')
    def post(self,request):
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
                        return render(request,'zhaohui.html',{'msg':'找回失败，请联系管理员，或者重新找回'})
                code = generate_verification_code(10)
                to_addr = email
                email = email
                code = code
                s = send_text(to_addr=to_addr, email=email, code=code)
                if s == 200:
                    User_ex.objects.create(email=email, valid_code=code)
                    return render(request,'chongzhi.html')
                return render(request, 'zhaohui.html', {'msg': '找回失败，请联系管理员，或者重新找回'})
            return render(request, 'zhaohui.html',{'msg':'邮箱不存在'})
        return render(request, 'zhaohui.html', {'msg': '用户名不存在'})
class RetpasswordView(View):
    def get(self,request):
        return render(request, 'chongzhi.html')
    def post(self,request):
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
        return render(request, 'chongzhi.html', {'msg': '邮箱不存在'})
class XiugaimimaView(View):
    def get(self,request):
        return render(request, 'xiugai.html')
    def post(self,request):
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
class XieboView(View):
    def get(self,request):
        if not request.session.get('username'):
            return HttpResponseRedirect('login')
        username = request.session['username']
        fen1 = Catagory.objects.all()
        return render(request, 'xiebo.html', {'fenlei_list': fen1})
    def post(self,request):
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
class ZhongxinView(View):
    def get(self,request,id):
        user=User.objects.get(id=str(id))
        post_list=Article.objects.filter(users__username=user)
        readlist=post_list.order_by('-click_count')[0:5]
        me=Article.objects.filter(is_recommend=True)
        tuijian_list=me.filter(users__username=user)
        return render(request,'geren.html',{'user':user,"post_list":post_list,'readlist':readlist,'tuijian_list':tuijian_list})
class ShangchuantouxiangView(View):
    def get(self,request):
        return render(request, 'xiu_touxiang.html')
    def post(self,request):
        try:
            username = request.session['username']
            photo = request.FILES['touxiang']
            try:
                be=User.objects.get(username__exact=username)
                be.avatar=photo
                return redirect('/')
            except Exception as e:
                return redirect('/gerenzhongxin')
            return render(request,'xiu_touxiang.html')
        except:
            return  redirect('/')
class BianjiView(View):
    def get(self,request,id):
        if not request.session.get('username'):
            return redirect('login')
        post_user = Article.objects.get(id=id)
        user = User.objects.get(username=request.session.get('username'))
        if user.id !=post_user:
            return  redirect('/')
        fenlei = Catagory.objects.all()
        user = User.objects.get(username=request.session.get('username'))
        return render(request, 'edit.html', {'post': post_user, 'fenlei_list': fenlei})
    def post(self,request,id):
        if  not request.session.get('username'):
            return  redirect('login')
        post_user=Article.objects.get(id=id)
        fenlei=Catagory.objects.all()
        user=User.objects.get(username=request.session.get('username'))
        title=request.POST['biaoti1']
        if len(title) <= 0:
            return render(request, 'xiebo.html', {'msg': "标题不能为空", 'fenlei_list': fenlei})
        content = request.POST['content']
        fenle = request.POST['jumpMenu']
        fen = Catagory.objects.get(name=fenle)
        if len(fenle) <= 0:
            return render(request, 'xiebo.html', {'msg': "标签不能为空", 'fenlei_list': fenlei})
        biaoqian_list = request.POST.getlist('checkbox')
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
        post_user.save()
        return  redirect('/')
@cache_page(60*15)
def pageNofoud(request):
    return render_to_response('404.html')
@cache_page(60*15)
def permission_denied(request):
    return render_to_response('403.html')