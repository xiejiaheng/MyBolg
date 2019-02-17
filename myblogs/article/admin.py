from django.contrib import admin
from .models import Article,Article_Kind,About
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','created_time')   #定制列
    ordering =('-id',)                                            #排序
    list_per_page = 5                                              #分页

@admin.register(Article_Kind)
class Article_KindAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    ordering =('-id',)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('id','tit','time')
    ordering =('-id',)
