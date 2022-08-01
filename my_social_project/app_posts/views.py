from django.shortcuts import HttpResponse,HttpResponseRedirect,render
from django.contrib.auth.decorators import login_required
from app_login.models import UserProfile,Follow
from django.contrib.auth.models import User
from app_posts.models import Post,Like
from app_posts.forms import CommentForm
from django.urls import reverse
# Create your views here.
@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post',flat=True)
    if request.method == 'GET':
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains=search)
    return render(request,'app_posts/home.html',context={'title':'Home','search':search,'result':result,'posts':posts,'liked_post_list':liked_post_list})

@login_required
def liked(request,pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    if not already_liked:
        liked_post = Like(post=post,user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unliked(request,pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))

@login_required
def comment(request,pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('app_posts:comment',kwargs={'pk':pk}))
    return render(request,'app_posts/comment.html',context={'comment_form':comment_form,'post':post})
    


