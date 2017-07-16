"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from blog.views import *
from django.conf.urls.static import static
from django.conf import  settings
urlpatterns = [
   #url(r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),

    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name=u'home'),
    url(r'^python$', python,name='python'),
    url(r'^ceshi$', ceshi,name='ceshi'),
    url(r'^dashuju$', dashuju,name='dashuju'),
    url(r'^guanli$', guanli,name='guanli'),
    url(r'^appium$', appium,name='appium'),
    url(r'^selenium$', selenium,name='selenium'),
    url(r'^mysql$', Mysql,name='mysql'),
    url(r'^git$', git,name='git'),
    url(r'^qianduan$', qianduan,name='qianduan'),
    url(r'^login$', login,name='login'),
    url(r'^reg$', reg,name='reg'),
    url(r'^(?P<id>\d+)/$',detail, name='detail'),
    url(r'^geren$', gerenzhongxin,name='geren'),
    url(r'^logout$', logout,name='logout'),
    url(r'^search$',blog_search, name = 'search'),
    url(r'^reset_pwd$', reset_pwd,name='reset_pwd'),
    url(r'^ret_passord$', ret_passord,name='ret_passord'),
    url(r'^xiugaimima$', xiugaimima,name='xiugaimima'),
    url(r'^xiebo$', xiebo,name='xiebo'),
    url(r'^zhongxi/(?P<id>\d+)/$', zhongxin,name='zhongxin'),
    url(r'^shangchuan$', shangchuantouxiang,name='shangchuan'),
    url(r'^bianji/(?P<id>\d+)/$',bianji,name='bianji')
]
