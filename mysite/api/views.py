from django.shortcuts import render
from django.http import JsonResponse
from .models import Post,User,Comment
# Create your views here.
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        # 用户注册
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print(request.POST)
        # print(username)
        # print(password)

        if not username or not password:
            return JsonResponse({'error': 'Username, password and email are required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=401)
        user = User(username=username, password=password)
        user.save()
        return JsonResponse({'code': 0})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def login(request):
    if request.method == 'POST':
        # 用户登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        # print(password)
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        try:
            user = User.objects.get(username=username, password=password)
            # 如果找到匹配的用户，则返回一个成功的响应
            return JsonResponse({'code': 0})
        except User.DoesNotExist:
            # 如果找不到匹配的用户，则返回一个401响应
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


def post(request):
    if request.method == 'GET':
        # 查询帖子
        posts = Post.objects.all()
        results = []
        for post in posts:
            result = {
                'postid':post.postid,
                'title': post.title,
                'content_type': post.content_type,
                'text': post.text,
                'media_url': post.media_url,
                'location_x': post.location_x,
                'location_y': post.location_y
            }
            results.append(result)
        return JsonResponse({'results': results})
    elif request.method == 'POST':
        # 创建帖子
        username = request.POST.get('username','')
        user = User.objects.get(username = username)
        title = request.POST.get('title', '')
        content_type = request.POST.get('content_type', '')
        text = request.POST.get('text', '')
        media_url = request.POST.get('media_url', '')
        location_x = request.POST.get('location_x', '')
        location_y = request.POST.get('location_y', '')
        post = Post(user=user,title=title, content_type=content_type, text=text, media_url=media_url, location_x=location_x, location_y=location_y)
        post.save()
        return JsonResponse({'code': 0})



def post_detail(request, postid):
    try:
        post = Post.objects.get(postid=postid)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post does not exist'}, status=404)
    if request.method == 'GET':
        # 显示某个帖子的具体信息
        result = {
            'postid':post.postid,
            'title': post.title,
            'content_type': post.content_type,
            'text': post.text,
            'media_url': post.media_url,
            'location_x': post.location_x,
            'location_y': post.location_y
        }
        return JsonResponse(result)
    elif request.method == 'PUT':
        # 更新某个帖子
        title = request.POST.get('title', '')
        content_type = request.POST.get('content_type', '')
        text = request.POST.get('text', '')
        media_url = request.POST.get('media_url', '')
        location_x = request.POST.get('location_x', '')
        location_y = request.POST.get('location_y', '')
        post.title = title if title else post.title
        post.content_type = content_type if content_type else post.content_type
        post.text = text if text else post.text
        post.media_url = media_url if media_url else post.media_url
        post.location_x = location_x if location_x else post.location_x
        post.location_y = location_y if location_y else post.location_y
        post.save()
        return JsonResponse({'code': 0})

def comment(request, postid):
    if request.method == 'GET':
        # 查看评论
        print(request)
        post = Post.objects.get(postid=postid)
        comments = Comment.objects.filter(post=post)
        result = []
        for comment in comments:
            result.append({
                'commentid':comment.commentid,
                'content_type': comment.content_type,
                'media_url': comment.media_url,
                'text': comment.text
            })
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        # 创建评论
        postid = request.POST.get('postid')
        post = Post.objects.get(postid=postid)
        content_type = request.POST.get('content_type')
        media_url = request.POST.get('media_url')
        text = request.POST.get('text')
        if not content_type or not text:
            return JsonResponse({'error': 'Content type and text are required.'}, status=400)
        comment = Comment(post=post,content_type=content_type, media_url=media_url, text=text)
        comment.save()
        return JsonResponse({'code': 0})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
