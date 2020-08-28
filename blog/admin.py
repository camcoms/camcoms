from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.core.mail import EmailMultiAlternatives
# Register your models here.
admin.site.site_header = "Camcoms后台管理"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'publisher',
        'pub_time',
        'is_publish',
        'view',
        'comment_num',
        'get_upload_url'
    )
    list_filter = (
        'pub_time',
        'is_publish',
        'publisher',
        'category'
    )
    list_display_links = ['title']
    ordering = ('-pub_time',)
    search_fields = ('title', 'publisher')
    filter_horizontal = ['category']
    list_per_page = 10

    def get_upload_url(self, obj):
        if obj.upload.url.endswith('.mp4') or obj.upload.url.endswith('.avi'):
            return format_html('<a href="{}"><img src="{}" style="width:50px;">\
                    </img></a>'.format(obj.upload.url, obj.upload_img.url))
        else:
            return format_html('<a href="{}"><img src={} style="width:50px;">\
                    </img></a>'.format(obj.upload.url, obj.upload.url))
    get_upload_url.short_description = '图片/视频'

    def save_model(self, request, obj, form, change):
        obj.publisher = request.user
        subs = [str(i) for i in Subscribe.objects.all()]
        subject = 'BACILLUS内容更新提醒：'
        message = obj.title
        href = 'http://127.0.0.1:8000/single/post/{}'.format(obj.id)
        html = '<a href={}>{}</a></br><p>{}</p><a href={}>Read more</a>'.format(href, message, obj.summary, href)
        msg = EmailMultiAlternatives(subject, message, 'Johnsons_yan@qq.com', bcc=subs)
        msg.attach_alternative(html, "text/html")
        msg.send()
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'kind', 'num')
    list_display_links = None
    actions = None


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'discussant', 'create_time', 'email', 'content')
    list_filter = ['create_time']
    list_display_links = ['discussant']

    def delete_model(self, request, obj):
        super(CommentAdmin, self).delete_model(request, obj)
        obj.post.get_comment_num()


@admin.register(Touch)
class TouchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'send_time')
    list_filter = ['send_time']
    list_display_links = ['name', 'email', 'phone']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']
    list_display_links = None


@admin.register(TestItem)
class TestItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'aswA', 'aswB', 'aswC', 'aswD', 'right_answer']
    list_per_page = 10
    list_display_links = ['title']
