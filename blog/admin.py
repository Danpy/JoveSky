# -*- coding: utf-8 -*-
"""
File: admin.py
Author: Jove Yu
Email: yushijun110@gmail.com
Github: https://github.com/JoveYu
Description: admin for blog app
"""
import markdown
from django.contrib import admin
from models import Tag,Page,Post,Link,Category,Image ,PostTag
from forms import PostForm,PageForm
from sitemap import ping_all_search_engines

class PostTagInline(admin.TabularInline):
    model = PostTag

class ImageAdmin(admin.ModelAdmin):
    list_display=['image']

class TagAdmin(admin.ModelAdmin):
    list_display=['name','count_post']
    inlines = (PostTagInline,)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']

class LinkAdmin(admin.ModelAdmin):
    list_display=['name','url']

class PageAdmin(admin.ModelAdmin):
    list_display=['title', 'get_absolute_url', 'author', 'create_time', 'seq']
    prepopulated_fields={"slug":("title",)}

    form = PageForm

    def save_model(self, request, obj, form, change):
        '''新建，修改页面'''
        obj.author=request.user
        obj.content = markdown.markdown(obj.markdown,['fenced_code', 'codehilite'])#(linenums=True)

        return super(PageAdmin,self).save_model(request, obj, form, change)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author', 'slug', 'counts', 'category', 'create_time']
    list_filter = ['author', 'tags']
    prepopulated_fields={"slug":("title",)}

    form = PostForm

    inlines = (PostTagInline,)

    def save_model(self, request, obj, form, change):

        #ping_google
        ping_all_search_engines()

        obj.author = request.user
        obj.content = markdown.markdown(obj.markdown,['fenced_code', 'codehilite'])
        return super(PostAdmin, self).save_model( request, obj, form, change)

admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Image, ImageAdmin)
