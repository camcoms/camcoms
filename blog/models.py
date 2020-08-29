from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from ckeditor.fields import RichTextField
from time import strftime, strptime
# from django.contrib import messages
# from django.utils.deconstruct import deconstructible
# Create your models here.
# username password email first_name last_name


formats = ['.mp4', '.jpg', '.jpeg', '.png', '.avi', '.JPG', 'JPEG', '.PNG']


class ActiveQuerySet(models.Manager):
    def get_queryset(self):
        return super(ActiveQuerySet, self).get_queryset().filter(is_publish=True)


class CommentManager(models.Manager):
    def get_queryset(self):
        return super(CommentManager, self).get_queryset().order_by('create_time')


class Category(models.Model):
    objects = models.Manager()
    Choices = (
        ('LifeStyle', 'LifeStyle'),
        ('Movie', 'Movie'),
        ('Literature', 'Literature'),
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Education', 'Education'),
        ('Internet', 'Internet'),
        ('Computer', 'Computer'),
        ('News', 'News'),
        ('Review', 'Review'),
    )
    kind = models.CharField(
        max_length=50,
        choices=Choices,
        unique=True,
        verbose_name='类别'
    )
    num = models.IntegerField(
        default=0,
        editable=False,
        verbose_name='文章数量'
    )

    def __str__(self):
        return self.kind

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = '类别'


class Post(models.Model):
    objects = models.Manager()
    title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name='标题'
    )
    upload = models.FileField(
        upload_to='%Y/%m/%d',
        verbose_name='图片/视频',
        help_text='请确保图片小于200KB，视频小于6MB！',
    )
    upload_img = models.ImageField(
        upload_to='%Y/%m/%d',
        help_text=format_html('<b style="color:red;">如果没有上传视频请不要上传这个图片，此图片将用作视频封面。</b>'),
        verbose_name='视频海报',
        blank=True,
        null=True,
        default='',
    )

    summary = models.CharField(
        max_length=300,
        blank=False,
        null=False,
        verbose_name='概述'
    )
    text = RichTextField(verbose_name='内容')
    pub_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发布时间'
    )
    view = models.IntegerField(
        default=0,
        editable=False,
        verbose_name='浏览量'
    )
    comment_num = models.IntegerField(
        default=0,
        editable=False,
        verbose_name='评论数'
    )
    category = models.ManyToManyField(
        Category,
        related_name='posts',
        related_query_name='post',
        verbose_name='标签'
    )
    saying = models.CharField(
        max_length=300,
        default="If you can't decide an saying who said it, then it was me!",
        verbose_name='名言引用'
    )
    note = models.CharField(
        max_length=300,
        default="随心所写，记录所想，往后翻起，才有念头！",
        verbose_name='作者随笔'
    )
    publisher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='作者'
    )
    is_publish = models.BooleanField(
        default=True,
        verbose_name='是否发布'
    )
    active_objects = ActiveQuerySet()

    def get_comment_num(self):
        comment_num = 0
        for cmt in self.comments.all():
            comment_num += 1
            try:
                for c in cmt.comment_set.all():
                    comment_num += 1
            except Exception:
                continue
        self.comment_num = comment_num
        self.save()
        return comment_num

    def get_time(self):
        t = str(self.pub_time).split('.')[0]
        return strftime('%a %b %d', strptime(t, '%Y-%m-%d %H:%M:%S'))

    def get_full_time(self):
        t = str(self.pub_time).split('.')[0]
        return strftime('%a %B %d, %Y', strptime(t, '%Y-%m-%d %H:%M:%S'))

    def get_date(self):
        t = str(self.pub_time).split('.')[0]
        return strftime('%Y-%m-%d', strptime(t, '%Y-%m-%d %H:%M:%S'))

    def is_video(self):
        if self.upload.name.endswith('.mp4') or self.upload.name.endswith('.avi'):
            return True
        return False

    def clean(self):
        flag = 0
        for i in formats:
            flag += 1
            if i not in self.upload.name and flag > len(formats):
                raise ValidationError(
                    '请上传本站支持格式的文件！'
                    'Rules_Broken',
                )
            if self.upload_img.name != '':
                if i not in self.upload_img.name and flag > len(formats):
                    raise ValidationError(
                        '请上传本站支持格式的文件！',
                        'Rules_Broken'
                    )
        if self.upload.name == '':
            raise ValidationError('请上传视频或图片！')
        if self.upload_img.name != '':
            if '.mp4' not in self.upload.name and '.avi' not in self.upload.name:
                raise ValidationError('图片不需要海报！', 'Rules_Broken')
        if self.upload_img.name == '':
            if '.mp4' in self.upload.name or '.avi' in self.upload.name:
                raise ValidationError('视频需要一个海报！', 'Rules_Broken')
        super(Post, self).clean()

    def __str__(self):
        return '{}、{}'.format(self.id, self.title)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'


class Comment(models.Model):
    time_manager = CommentManager()
    content = models.TextField(
        verbose_name='评论内容'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment',
        verbose_name='所属',
        blank=True,
        null=True
    )
    com = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='自评论',
        blank=True,
        null=True
    )
    discussant = models.CharField(
        max_length=100,
        verbose_name='评论人'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='评论时间'
    )
    email = models.EmailField(verbose_name='邮箱')

    def get_full_time(self):
        t = str(self.create_time).split('.')[0]
        return strftime('%a %B %d, %Y', strptime(t, '%Y-%m-%d %H:%M:%S'))

    def get_date(self):
        t = str(self.create_time).split('.')[0]
        return strftime('%Y-%m-%d', strptime(t, '%Y-%m-%d %H:%M:%S'))

    def __str__(self):
        return self.content

    def clean(self):
        if self.post and self.com:
            raise ValidationError('“所属”和“自评论”不可同时填充')
        if not self.post and not self.com:
            raise ValidationError('“所属”和“自评论”必选其一')
        super(Comment, self).clean()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Comment, self).save()
        if self.post:
            self.post.get_comment_num()
            self.post.save()
        if self.com:
            self.com.post.get_comment_num()
            self.com.post.save()

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'


class Touch(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='联系人'
    )
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='手机号',
    )
    website = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='网站'
    )
    message = models.TextField(
        verbose_name='消息内容'
    )
    send_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='发送时间'
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '联系'
        verbose_name_plural = '联系'


class Subscribe(models.Model):
    email = models.EmailField(verbose_name='邮箱')
    objects = models.Manager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '订阅'
        verbose_name_plural = '订阅'


class TestItem(models.Model):
    objects = models.Manager()
    title = models.TextField(verbose_name='标题')
    content = models.TextField(verbose_name='可选答案')
    right_answer = models.TextField(verbose_name='答案')

    class Meta:
        verbose_name = '考试题'
        verbose_name_plural = '考试题'
