# -*- coding:utf-8 -*-  
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
import datetime,time
class ArticleManager(models.Manager):
    def distinct_date(self):
        distint_daye_lisy=[]
        date_list=self.values('date_publish')
        for date in date_list:
            date=date['date_publish'].strftime('%Y/%m')
            if date not  in distint_daye_lisy:
                distint_daye_lisy.append(date)
        return distint_daye_lisy
class User(AbstractUser):
    avatar=models.ImageField(upload_to='vaatar/%Y/%m',default='vaatar/default/pang')
    qq=models.CharField(u'qq号码', max_length=20,blank=True)
    mobile=models.CharField(u'手机号',max_length=11,blank=True,null=True,unique=True)
    login_sta = models.CharField(u'登录是否锁定', max_length=2, default=0)
    login_suo = models.DateTimeField(u'登录锁定时间', default=datetime.datetime.now())
    is_login = models.BooleanField(default=False)
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name
        ordering=['-id']
    def __str__(self) :
        return self.username
class Tag(models.Model):
    name=models.CharField(u'标签名',max_length=30)
    class Meta:
        verbose_name=u'标签'
        verbose_name_plural=verbose_name
    def __str__(self) :
        return self.name
class Catagory(models.Model):
    name = models.CharField(u'分类', max_length=30)
    index=models.IntegerField(u'分类排序',default=999)
    class Meta:
        verbose_name=u'分类'
        verbose_name_plural=verbose_name
    def __str__(self) :
        return self.name
    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path
class Article(models.Model):
    title=models.CharField(u'文章标题',max_length=50)
    desc=models.CharField(u'文章描述',max_length=50)
    content=models.TextField(u'文章内容')
    click_count=models.IntegerField(u'点击次数',default=0)
    date_publish=models.DateTimeField(u'发布时间',auto_now_add=True)
    is_recommend=models.BooleanField(u'是否推荐',default=False)
    users=models.ForeignKey(User)
    categorys=models.ForeignKey(Catagory)
    tag=models.ManyToManyField(Tag)
    objects=ArticleManager()
    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
        ordering=['-date_publish']
    def __str__(self) :
        return self.title
    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path
class Comment(models.Model):
    content=models.TextField(u'评论内容')
    date_publish=models.DateTimeField(u'评论时间',auto_now_add=True)
    user=models.ForeignKey(User,blank=True,null=True)
    article=models.ForeignKey(Article,blank=True,null=True)
    pid=models.ForeignKey('self',blank=True,null=True)
    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']
    def __str__(self):
        return str(self.id)
class Links(models.Model):
    title=models.CharField(u'标题',max_length=50)
    description=models.CharField(u'友情链接描述',max_length=200)
    callback_url=models.URLField(u'url地址')
    index=models.IntegerField(u'排列顺序',default=999)
    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']
    def __str__(self):
        return self.title
class Ad(models.Model):
    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(u'广告描述', max_length=200)
    image_url=models.ImageField(u'图片路径',upload_to='%d/%Y/%m')
    callback_url = models.URLField(u'回调url地址',blank=True,null=True)
    date_publish = models.DateTimeField(u'发布时间', auto_now_add=True)
    index = models.IntegerField(u'排列顺序', default=999)
    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
    def __str__(self) :
        return self.title
class User_ex(models.Model):
    """User models ex"""
    email = models.EmailField(unique=True, blank=False, null=False)
    valid_code = models.CharField(max_length=24)   #验证码
    valid_time = models.DateTimeField(auto_now=True)   #验证码有效时间
    class Meta:
        verbose_name = u'验证码'
        verbose_name_plural = u"验证码"
    def __str__(self):
        return u'%s' % self.valid_code
class Usernam(models.Model):
    users = models.CharField(max_length=10)
    guanzhu_zhe=models.ManyToManyField(User)
    class Meta:
        verbose_name = u'关注'
        verbose_name_plural = verbose_name
    def __str__(self):
        return u'%s' % self.users
class Ip(models.Model):
    ip=models.CharField(max_length=20)
    time=models.DateTimeField()
    class Meta:
        verbose_name = u'访问时间'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.ip
