from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
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
    qq=models.CharField('qq号码', max_length=20,blank=True)
    mobile=models.CharField('手机号',max_length=11,blank=True,null=True,unique=True)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering=['-id']
    def __str__(self) :
        return self.username
class Tag(models.Model):
    name=models.CharField('标签名',max_length=30)
    class Meta:
        verbose_name='标签'
        verbose_name_plural=verbose_name
    def __str__(self) :
        return self.name
class Catagory(models.Model):
    name = models.CharField('分类', max_length=30)
    index=models.IntegerField('分类排序',default=999)
    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name
    def __str__(self) :
        return self.name
    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path
class Article(models.Model):
    title=models.CharField('文章标题',max_length=50)
    desc=models.CharField('文章描述',max_length=50)
    content=models.TextField('文章内容')
    click_count=models.IntegerField('点击次数',default=0)
    date_publish=models.DateTimeField('发布时间',auto_now_add=True)
    is_recommend=models.BooleanField('是否推荐',default=False)
    users=models.ForeignKey(User)
    categorys=models.ForeignKey(Catagory)
    tag=models.ManyToManyField(Tag)
    objects=ArticleManager()
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering=['-date_publish']
    def __str__(self) :
        return self.title
    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path
class Comment(models.Model):
    content=models.TextField('评论内容')
    date_publish=models.DateTimeField('评论时间',auto_now_add=True)
    user=models.ForeignKey(User,blank=True,null=True)
    article=models.ForeignKey(Article,blank=True,null=True)
    pid=models.ForeignKey('self',blank=True,null=True)
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']
    def __str__(self):
        return str(self.id)
class Links(models.Model):
    title=models.CharField('标题',max_length=50)
    description=models.CharField('友情链接描述',max_length=200)
    callback_url=models.URLField('url地址')
    date_publish = models.DateTimeField('评论时间', auto_now_add=True)
    index=models.IntegerField('排列顺序',default=999)
    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']
    def __str__(self):
        return self.title
class Ad(models.Model):
    title = models.CharField('广告标题', max_length=50)
    description = models.CharField('广告描述', max_length=200)
    image_url=models.ImageField('图片路径',upload_to='%d/%Y/%m')
    callback_url = models.URLField('回调url地址',blank=True,null=True)
    date_publish = models.DateTimeField('发布时间', auto_now_add=True)
    index = models.IntegerField('排列顺序', default=999)
    class Meta:
        verbose_name = '广告'
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
        verbose_name = '关注'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u'%s' % self.users
