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
    url(r'^$', home, name=u'首页'),
    url(r'^python', python),
    url(r'^ceshi', ceshi),
    url(r'^dashuju', dashuju),
    url(r'^guanli', guanli),
    url(r'^appium', appium),
    url(r'^selenium', selenium),
    url(r'^mysql', Mysql),
    url(r'^git', git),
    url(r'^qianduan', qianduan),
    url(r'^login', login),
    url(r'^reg', reg),
    url(r'^(?P<id>\d+)/$',detail, name='detail'),
    url(r'^geren', gerenzhongxin),
    url(r'^logout', logout),
    url(r'^search/$',blog_search, name = 'search'),
    url(r'^reset_pwd', reset_pwd),
    url(r'^ret_passord', ret_passord),
    url(r'^xiugaimima', xiugaimima),
    url(r'^xiebo', xiebo),
    url(r'^zhongxi/(?P<id>\d+)/$', zhongxin,name='zhongxin'),
    url(r'^shangchuan', shangchuantouxiang),
]
