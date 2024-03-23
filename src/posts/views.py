from django.shortcuts import render
from .models import Post
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
def post_list_and_create(request):
    qs = Post.objects.all()
    return render(request, 'posts/main.html', {'qs':qs})

def load_post_data_view(request, num_posts):
    visible = 3
    upper = num_posts
    lower = upper - visible
    size = Post.objects.all().count()

    qs = Post.objects.all()
    data = []
    for obj in qs:
        item = {
            'id': obj.id,
            'title': obj.title,
            'body': obj.body,
            #'liked': True if request.user in obj.liked.all() else False,
            'liked': True if request.user.is_authenticated and request.user in obj.liked.all() else False,  # Check if the user is authenticated
            'count': obj.like_count,
            'author':obj.author.user.username
        }
        data.append(item)
    return JsonResponse({'data':data[lower:upper], 'size': size})

# def like_unlike_post(request):
#     if request.is_ajax():
#         pk = request.POST.get('pk')
#         obj = Post.objects.get(pk=pk)
#         if request.user in obj.liked.all():
#             liked = False
#             obj.liked.remove(request.user)
#         else:
#             liked = True
#             obj.liked.add(request.user)
#         return JsonResponse({'liked': liked, 'count': obj.like_count})

@ensure_csrf_cookie  # Ensure that CSRF cookie is set
def like_unlike_post(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's a POST request and AJAX
        pk = request.POST.get('pk')
        obj = Post.objects.get(pk=pk)
        if request.user.is_authenticated:
            if request.user in obj.liked.all():
                liked = False
                obj.liked.remove(request.user)
            else:
                liked = True
                obj.liked.add(request.user)
            return JsonResponse({'liked': liked, 'count': obj.like_count})
        else:
            return JsonResponse({'error': 'User not authenticated'}, status=403)  # Return error if user is not authenticated
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)  # Return error for invalid request


def hello_world_view(request):
    return JsonResponse({'text': 'hello world'})
