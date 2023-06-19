from django.shortcuts import render,redirect, get_object_or_404
from .models import Post, Profile, Images
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.contrib import auth
import datetime as dt
from .models import CommentData

def post_list(request):
    posts_list = Post.objects.all().order_by('-id')
    query = request.GET.get('query')
    if query:
        posts = Post.objects.filter(
        Q(title__contains = query) |
        Q(author__username = query) |
        Q(body__contains = query)
        )
    paginator = Paginator(posts_list,4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post_list.html',{'posts':posts})

def post_detail(request,id,slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post':post,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
    }
    
    return render(request,'post_detail.html',context)

def comment(request):
    data = CommentData.objects.all()  # CommentData.objects.all().order_by('-id')
    lst = []
    for i in data:
        lst.insert(0,i)
    if request.method == 'GET':
        return render(request,'comment.html',{'data':lst},)
    else:
        CommentData(
        comment = request.POST['com'],
        date = dt.datetime.now()
        ).save()
        return redirect('post_list')

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())

def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/post_list')
    else:
        form = PostCreateForm()
        return render(request,'post_create.html',{'form':form})


def login_artical(request):
    post = Post.objects.all()
    return render(request,'login_artical.html',{'post':post})

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

def user_logout(request):
    logout(request)
    return redirect('/post_list')

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username1 = request.POST['username']
            password1 = request.POST['password']
            user = authenticate(username=username1, password=password1)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('loginhome')
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("User is None")
    else:
        form = UserLoginForm()
        return render(request, 'login.html',{'form':form})

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('user_login')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

def loginhome(request):
    return render(request,'loginhome.html')





def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('/post_list')
    else:
        form = UserRegistrationForm()
        return render(request, 'register.html',{'form':form})


def edit_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/post_list')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'edit_profile.html',{'user_form':user_form, 'profile_form':profile_form})

def post_edit(request,id):
    user = request.user.id
    post = get_object_or_404(Post, id=id)
    if user == post.author_id:
        if request.method == "POST":
            form = PostEditForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = PostEditForm(instance=post)
            return render(request, 'post_edit.html',{'form':form})
    else:
        return HttpResponse("your a different user")


def post_delete(request,id):
    user = request.user.id
    post = Post.objects.get(id=id)
    if user == post.author_id:
        post.delete()
        return redirect('post_list')
    else:
        return HttpResponse("your a different user thats why yo can't delete")



