from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.core.mail import send_mail
from .models import Post, Category, Touch, Subscribe, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
import json
# Create your views here.


class Counter:
    def __init__(self):
        self.start = 0

    def get_counter(self):
        self.start += 1
        return self.start


def get_count(s):
    queryset = Category.objects.all()
    count = len(queryset.filter(kind__icontains=s)[0].posts.all())
    return count


def get_post(s):
    queryset = Category.objects.all()
    post = queryset.filter(kind__icontains=s)[0].posts.all()
    return post


def index(request):
    ls = get_count('LifeStyle')
    mv = get_count('Movie')
    lt = get_count('Literature')
    sp = get_count('Sports')
    mu = get_count('Music')
    ed = get_count('Education')
    it = get_count('Internet')
    cp = get_count('Computer')
    nw = get_count('News')
    rev = get_count('Review')
    page_num = 1
    if request.method == 'GET':
        try:
            page_num = int(request.GET['page'])
        except KeyError:
            page_num = 1
    post0 = Post.objects.filter(upload_img='')[0]
    try:
        recents = Post.objects.order_by('-pub_time')[0:3]
        populars = Post.objects.order_by('-view')[:2]
    except IndexError:
        recents = Post.objects.order_by('-pub_time')[0:2]
        populars = Post.objects.order_by('-view')[:2]
    posts = Post.objects.all()
    video_page = Paginator(list(posts.filter(upload__endswith='.mp4').order_by('-pub_time')), 1)
    image_page = Paginator(list(posts.exclude(upload__endswith='.mp4').order_by('-pub_time')), 7)
    try:
        page = image_page.page(page_num)
    except PageNotAnInteger:
        page = image_page.page(1)
    except EmptyPage:
        page = image_page.page(image_page.num_pages)
    try:
        vpage = video_page.page(page_num)
    except PageNotAnInteger:
        vpage = video_page.page(1)
    except EmptyPage:
        vpage = video_page.page(video_page.num_pages)
    try:
        p1 = page[0]
    except IndexError:
        p1 = False
    try:
        p2 = page[1]
    except IndexError:
        p2 = False
    try:
        p3 = page[2]
    except IndexError:
        p3 = False
    try:
        p4 = page[3]
    except IndexError:
        p4 = False
    try:
        p5 = page[4]
    except IndexError:
        p5 = False
    try:
        p6 = page[5]
    except IndexError:
        p6 = False
    try:
        p7 = page[6]
    except IndexError:
        p7 = False
    vp = vpage[0]
    flag = True
    if image_page.num_pages-1 == page_num:
        flag = False
    return render(request, 'blog/index.html', locals())


def single(request, post_id=8):
    try:
        post = Post.objects.get(pk=post_id)
    except Exception:
        raise Http404
    post.view = int(post.view)+1
    post.save()
    comments = list(post.comments.all().order_by('create_time'))
    counter = Counter()
    pts = post.category.all()[0].posts.all()
    arrs = []
    try:
        recents = Post.objects.order_by('-pub_time').exclude(upload__iendswith='.mp4')[:3]
        populars = Post.objects.order_by('-view').exclude(upload__iendswith='.mp4')[:3]
    except IndexError:
        recents = Post.objects.order_by('-pub_time').exclude(upload__iendswith='.mp4')[:2]
        populars = Post.objects.order_by('-view').exclude(upload__iendswith='.mp4')[:2]
    for i in pts:
        if i.id != post_id and len(arrs) <= 2:
            arrs.append(i)
        if len(arrs) >= 2:
            break
    if post.upload.name.endswith('.mp4'):
        temp = 'blog/vsingle.html'
    else:
        temp = 'blog/single.html'
    return render(
        request,
        temp,
        locals()
    )


def archive(request):
    try:
        recents = Post.objects.order_by('-pub_time').exclude(upload__iendswith='.mp4')[:3]
        populars = Post.objects.order_by('-view').exclude(upload__iendswith='.mp4')[:3]
    except IndexError:
        recents = Post.objects.order_by('-pub_time').exclude(upload__iendswith='.mp4')[:2]
        populars = Post.objects.order_by('-view').exclude(upload__iendswith='.mp4')[:2]
    kind = ''
    page_num = 1
    if request.method == 'GET':
        try:
            kind = request.GET['kind']
        except KeyError:
            kind = 'LifeStyle'
        try:
            page_num = int(request.GET['page'])
        except KeyError:
            page_num = 1
    queryset = Category.objects.all()
    kind_posts = queryset.filter(kind__icontains=kind)[0].posts.all()
    all_page = Paginator(list(kind_posts), 6)
    try:
        page = all_page.page(page_num)
    except PageNotAnInteger:
        page = all_page.page(1)
    except EmptyPage:
        page = all_page.page(all_page.num_pages)
    flag = True
    if all_page.num_pages - 1 == page_num:
        flag = False
    return render(request, 'blog/archive.html', locals())


def contact(request):
    return render(request, 'blog/contact.html')


def contact_rec_email(request):
    try:
        if request.method == 'POST':
            name = request.POST['author']
            email = request.POST['email']
            phone = request.POST['tel'] if request.POST['tel'] else '未填写'
            message = request.POST['comment']
            url = request.POST['url'] if request.POST['url'] else '未填写'
            touch = Touch(name=name, email=email, phone=phone, message=message, website=url)
            touch.save()
            subject = '来自{}({}):'.format(name, email)
            send_mail(
                subject,
                message,
                'Johnsons_yan@qq.com',
                ['johnsons_yan@163.com', '2633839011@qq.com'],
            )
    except KeyError:
        messages.add_message(request, messages.INFO, '发送失败，请稍后重试')
        return redirect('/')
    except Exception:
        messages.add_message(request, messages.INFO, '网络出错，请稍后重试')
        return redirect('/')
    messages.add_message(request, messages.INFO, '发送成功')
    return redirect('/')


def comment(request):
    json_data = ''
    try:
        if request.method == 'POST':
            author = request.POST['author']
            email = request.POST['email']
            content = request.POST['comment']
            cid = int(request.POST['id'])
            com = Comment.time_manager.get(pk=cid)
            self_comment = Comment(content=content, com=com, discussant=author, email=email)
            self_comment.save()
            data = {
                'author': self_comment.discussant,
                'content': self_comment.content,
                'comment_num': self_comment.com.post.get_comment_num(),
                'date': self_comment.get_date(),
                'time': self_comment.get_full_time(),
                'result': '评论成功'
            }
            json_data = json.dumps(data)
    except KeyError:
        return HttpResponseBadRequest
    return HttpResponse(json_data, content_type='application/json')


def comment_post(request):
    json_data = ''
    try:
        if request.method == 'POST':
            author = request.POST['author']
            email = request.POST['email']
            content = request.POST['comment']
            pid = int(request.POST['id'])
            post = Post.objects.get(pk=pid)
            new_comment = Comment(content=content, post=post, discussant=author, email=email)
            new_comment.save()
            data = {
                'author': new_comment.discussant,
                'content': new_comment.content,
                'comment_num': post.get_comment_num(),
                'date': new_comment.get_date(),
                'time': new_comment.get_full_time(),
                'comment_id': new_comment.id,
                'result': '评论成功'
            }
            json_data = json.dumps(data)
    except KeyError:
        return HttpResponseBadRequest
    return HttpResponse(json_data, content_type='application/json')


# 改成ajax
def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Subscribe.objects.filter(email__icontains=email):
            json_data = json.dumps({'result': '已经订阅，请勿重复订阅'})
            return HttpResponse(json_data, content_type='application/json')
        sub = Subscribe(email=email)
        try:
            send_mail(
                '订阅通知:',
                '感谢您的订阅，网站更新内容后将会自动发送通知给您！',
                'Johnsons_yan@qq.com',
                [email],
            )
            sub.save()
        except Exception:
            json_data = json.dumps({'result': '订阅失败，请重试'})
            return HttpResponse(json_data, content_type='application/json')
        else:
            json_data = json.dumps({'result': '订阅成功'})
            return HttpResponse(json_data, content_type='application/json')


def search(request):
    import time
    time.sleep(5)
    return redirect('/')
