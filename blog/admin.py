#from django.contrib import admin
from blog.models import *
from public import xadmin
# Register your models here.
# class ArticleAdmin(admin.ModelAdmin):
#     #fields = ('title','desc','content')
#     list_display = ('title','users','date_publish')
#     list_display_links = ('title', 'users', 'date_publish')
#     class Media:
#         js = (
#             'js/kindeditor-4.1.10/kindeditor-all-min.js',
#             'js/kindeditor-4.1.10/lang/zh_CN.js',
#             'js/kindeditor-4.1.10/config.js',
#         )
# class User_exAdmin(admin.ModelAdmin):
#     list_display = ('email', 'valid_code', 'valid_time')
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'username','qq','mobile')
# class LinkAdmin(admin.ModelAdmin):
#     list_display = ('title','callback_url')
# admin.site.register(User,UserAdmin)
# admin.site.register(Article,ArticleAdmin)
# admin.site.register(Tag)
# admin.site.register(Catagory)
# admin.site.register(Comment)
# admin.site.register(Links,LinkAdmin)
# admin.site.register(Ad)
# admin.site.register(User_ex,User_exAdmin)
# admin.site.register(Usernam)
xadmin.site.register(Tag)
xadmin.site.register(Article)
xadmin.site.register(Catagory)
xadmin.site.register(Comment)
xadmin.site.register(Links)
xadmin.site.register(Ad)
xadmin.site.register(User_ex)
xadmin.site.register(Usernam)
# xadmin.site.register(Ip)
