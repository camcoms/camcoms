# Generated by Django 3.0.8 on 2020-08-05 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('LifeStyle', 'LifeStyle'), ('Movie', 'Movie'), ('Literature', 'Literature'), ('Sports', 'Sports'), ('Music', 'Music'), ('Education', 'Education'), ('Internet', 'Internet'), ('Computer', 'Computer'), ('News', 'News'), ('Review', 'Review')], max_length=50, unique=True, verbose_name='类别')),
                ('num', models.IntegerField(default=0, editable=False, verbose_name='文章数量')),
            ],
            options={
                'verbose_name': '类别',
                'verbose_name_plural': '类别',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='Touch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='联系人')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=20, verbose_name='手机号')),
                ('website', models.CharField(default='www.worldwideweb.com', max_length=100, verbose_name='网站')),
                ('message', models.CharField(max_length=1000, verbose_name='消息内容')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': 'Contact Me',
                'verbose_name_plural': 'Contact Me',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('upload', models.FileField(default='2020/08/05/ckin.jpg', help_text='每篇文章都需要一张图片或短视频，并且确保单个文件的大小在10MB以内！', upload_to='%Y/%m/%d', verbose_name='图片/视频')),
                ('upload_img', models.ImageField(default='', help_text='<b style="color:red;">如果没有上传视频请不要上传这个图片，此图片将用作视频封面。</b>', upload_to='%Y/%m/%d', verbose_name='视频海报')),
                ('summary', models.CharField(max_length=500, verbose_name='概述')),
                ('text', models.TextField(verbose_name='内容')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('view', models.IntegerField(default=0, editable=False, verbose_name='浏览量')),
                ('comment_num', models.IntegerField(default=0, editable=False, verbose_name='评论数')),
                ('saying', models.CharField(default="If you can't decide an saying who said it, then it was me!", max_length=500, verbose_name='名言引用')),
                ('note', models.CharField(default='随心所写，记录所想，往后翻起，才有念头！', max_length=500, verbose_name='作者随笔')),
                ('is_publish', models.BooleanField(default=True, verbose_name='是否发布')),
                ('category', models.ManyToManyField(related_name='posts', related_query_name='post', to='blog.Category', verbose_name='标签')),
                ('publisher', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500, verbose_name='评论')),
                ('discussant', models.CharField(max_length=100, verbose_name='评论人')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('com', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='自评论')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', related_query_name='comment', to='blog.Post', verbose_name='所属')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
