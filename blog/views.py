from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator
from blog.forms import PostForm
from blog.models import Post, Comment, Follow, Like
from register.models import User


def blog_index(request):
    user = request.user
    return render(request, 'blog_index.html', {'user': user})


def post_list(request):
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = Post.objects.filter(tags__slug=tag_slug)
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 10)  # 每页显示 10 篇文章

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()
    return render(request, 'post_list.html', {'page_obj': page_obj, 'tags': tags})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # 查询点赞数量
    likes_count = Like.objects.filter(post=post).count()
    # 查询评论数量
    comments_count = Comment.objects.filter(post=post).count()

    shares = post.shares



    return render(request, 'post_detail.html',
                  {'post': post, 'shares': shares, 'likes_count': likes_count, 'comments_count': comments_count,
                   })


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    # 检查是否已经点赞
    if Like.objects.filter(user=user, post=post).exists():
        # 如果已经点赞，执行取消点赞操作
        Like.objects.filter(user=user, post=post).delete()
    else:
        # 如果尚未点赞，执行点赞操作
        Like.objects.create(user=user, post=post)

    return redirect('blog:post_detail', post_id=post_id)


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    content = request.POST.get('content')

    if not content:
        error_message = "评论内容不能为空"
        return render(request, 'post_detail.html',
                      {'post': post, 'shares': post.shares, 'error_message': error_message})

    Comment.objects.create(user=user, post=post, content=content)

    return redirect('blog:post_detail', post_id=post_id)


def share_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        post.shares += 1
        post.save()
    return redirect('blog:post_detail', post_id=post_id)


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user)
    followers = user.get_followers()
    following = user.get_following()
    return render(request, 'user_profile.html',
                  {'user': user, 'followers': followers, 'following': following, 'posts': posts})


def search_posts(request):
    query = request.GET.get('q')
    posts = None

    if query:
        posts = Post.objects.filter(title__icontains=query)

    return render(request, 'search_results.html', {'query': query, 'posts': posts})


@login_required
def follow_user(request, user_id):
    following_user = get_object_or_404(User, id=user_id)
    follower_user = request.user

    # 检查是否已经关注
    if Follow.objects.filter(follower=follower_user, following=following_user).exists():
        # 如果已经关注，执行取消关注操作
        Follow.objects.filter(follower=follower_user, following=following_user).delete()
    else:
        # 如果尚未关注，执行关注操作
        Follow.objects.create(follower=follower_user, following=following_user)

    return redirect('blog:user_profile', user_id=user_id)


def follower_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.get_followers()
    return render(request, 'followers_list.html', {'user': user, 'followers': followers})


def following_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = user.get_following()
    return render(request, 'following_list.html', {'user': user, 'following': following})


def post_likes(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(post=post)
    return render(request, 'likes_list.html', {'post': post, 'likes': likes})


def comments_list(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # 获取评论对象列表
    comments = Comment.objects.filter(post=post)

    # 使用分页器对评论进行分页
    paginator = Paginator(comments, 5)  # 每页显示 5 条评论

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'comments_list.html', {'post': post, 'comments': comments,'page_obj': page_obj})
