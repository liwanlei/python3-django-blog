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

from django.conf.urls import url,include
from django.contrib import admin
from blog.views import *
from django.conf.urls.static import static
from django.conf import  settings
from public.xadmin.plugins import  xversion
from public import xadmin
from django.views.decorators.cache import cache_page
xversion.register_models()
xadmin.autodiscover()
urlpatterns = [
   #url(r'^uploads/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),

    #url(r'^admin/', admin.site.urls),
    url(r'^$', cache_page(60*2)(HomeView.as_view()), name='home'),
    url(r'^python$', python,name='python'),
    url(r'^ceshi$', ceshi,name='ceshi'),
    url(r'^dashuju$', dashuju,name='dashuju'),
    url(r'^guanli$', guanli,name='guanli'),
    url(r'^appium$', appium,name='appium'),
    url(r'^selenium$', selenium,name='selenium'),
    url(r'^mysql$', Mysql,name='mysql'),
    url(r'^git$', git,name='git'),
    url(r'^qianduan$', qianduan,name='qianduan'),
    url(r'^login$', cache_page(60*30)(LoginView.as_view()),name='login'),
    url(r'^reg$', cache_page(60*30)(RegView.as_view()),name='reg'),
    url(r'^(?P<id>\d+)/$',DetailView.as_view(), name='detail'),
    url(r'^person$', GerenzhongxinView.as_view(),name='person'),
    url(r'^logout$', LoginView.as_view(),name='logout'),
    url(r'^search$',BlogSearchView.as_view(), name = 'search'),
    url(r'^reset_pwd$', ResetpwdView.as_view(),name='reset_pwd'),
    url(r'^ret_passord$', RetpasswordView.as_view(),name='ret_passord'),
    url(r'^xiugaimima$', XiugaimimaView.as_view(),name='xiugaimima'),
    url(r'^xiebo$', XieboView.as_view(),name='xiebo'),
    url(r'^zhongxi/(?P<id>\d+)/$', ZhongxinView.as_view(),name='zhongxin'),
    url(r'^shangchuan$',ShangchuantouxiangView.as_view(),name='shangchuan'),
    url(r'^bianji/(?P<id>\d+)/$',BianjiView.as_view(),name='bianji'),
    url(r'xadmin/', include(xadmin.site.urls)),
]
