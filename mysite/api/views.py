from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post,User
# Create your views here.
from django.contrib.auth import authenticate, login

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 用户注册
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not username or not password or not email:
            return JsonResponse({'error': 'Username, password and email are required.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 用户登录
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def post(request):
    if request.method == 'GET':
        # 查询帖子
        posts = Post.objects.all()
        results = []
        for post in posts:
            result = {
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
        title = request.POST.get('title')
        content_type = request.POST.get('content_type')
        text = request.POST.get('text')
        media_url = request.POST.get('media_url')
        location_x = request.POST.get('location_x')
        location_y = request.POST.get('location_y')
        post = Post(title=title, content_type=content_type, text=text, media_url=media_url, location_x=location_x, location_y=location_y)
        post.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post does not exist'}, status=404)
    if request.method == 'GET':
        # 显示某个帖子的具体信息
        result = {
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
        title = request.POST.get('title')
        content_type = request.POST.get('content_type')
        text = request.POST.get('text')
        media_url = request.POST.get('media_url')
        location_x = request.POST.get('location_x')
        location_y = request.POST.get('location_y')
        post.title = title if title else post.title
        post.content_type = content_type if content_type else post.content_type
        post.text = text if text else post.text
        post.media_url = media_url if media_url else post.media_url
        post.location_x = location_x if location_x else post.location_x
        post.location_y = location_y if location_y else post.location_y
        post.save()
        return JsonResponse({'status': 'success'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comment

@csrf_exempt
def comment(request, post_id):
    if request.method == 'GET':
        # 查看评论
        comments = Comment.objects.filter(post_id=post_id)
        result = []
        for comment in comments:
            result.append({
                'content_type': comment.content_type,
                'media_url': comment.media_url,
                'text': comment.text
            })
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        # 创建评论
        content_type = request.POST.get('content_type')
        media_url = request.POST.get('media_url')
        text = request.POST.get('text')
        if not content_type or not text:
            return JsonResponse({'error': 'Content type and text are required.'}, status=400)
        comment = Comment(content_type=content_type, media_url=media_url, text=text, post_id=post_id)
        comment.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
