from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.

from .forms import *

def register_view(request):
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
      try:
        form.save()
        messages.info(request,'Account created successfully')
        return redirect("login")
      except ValueError:
        messages.error(request,'Account with that username already exists. Pick another username')
  context = {
    "form": form,
  }
  return render(request, "register.html", context)

def login_view(request):
  if(request.method == "POST"):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    user1 = User.objects.filter(username = username).filter(password = password)
    print(user1)
    if(user is not None):
      login(request, user)
      return redirect('home')
    else:
      print("not authenticated")
  return render(request, "login.html")

def home(request):
  follows = Follower.objects.all()
  exclude_list = [request.user]
  account = Account.objects.get(user = request.user)
  account_list = [account]
  for i in follows:
    if(str(i.follower_id) == str(request.user.username)):
      user_instance = User.objects.get(username = str(i.followee_id))
      account_instance = Account.objects.get(user = user_instance)
      exclude_list.append(user_instance)
      account_list.append(account_instance)
  accounts = Account.objects.exclude(user__in = exclude_list)
  account_search = accounts
  value =""
  
  # PostImageFormset = inlineformset_factory(Account, Post, form = PostForm, extra=1)
  # account = Account.objects.get(user = request.user)
  # formset = PostImageFormset(queryset = Post.objects.none(), instance = account)
  # initial_dict = {
  #       "user_id" : account,
  #   }
  post_form = PostForm()



  if request.method == "POST":
    if request.POST.get('searched'):
      print(request.POST)
      search = request.POST.get('searched',False)
      value = search
      account_search = Account.objects.filter(user__username__icontains=search)
  # print(accounts.count())
  # count = accounts.count()
  # print(f'count - {count}')
  posts = Post.objects.none()
  following = Follower.objects.none()
  likes = Like.objects.none()
  likes_list = []
  # if count:
  count = Post.objects.filter(user_id__in = account_list).count()
  posts = reversed(Post.objects.filter(user_id__in = account_list).order_by('created_at'))
  following = Follower.objects.filter(follower_id = account)
  follower = Follower.objects.filter(followee_id = account)
  likes = Like.objects.filter(liked_by = request.user.account)
  my_likes = Like.objects.filter(user_id = request.user.account)
  

  for i in likes:
    likes_list.append(i.post_id.post)
  comments_form = CommentForm()

  context = {
    "accounts": accounts,
    "count": count,
    "following": following,
    "follower": follower,
    "likes": likes,
    "likes_list": likes_list,
    "posts": posts,
    "account_search": account_search,
    "value": value,
    "post_form": post_form,
    "comments_form": comments_form,
    "my_likes": my_likes,
  }
  return render(request, "home.html", context = context)





def your_profile(request):
  return render(request, "your-profile.html")

def post_modal_view(request):
  return render(request, "post-modal.html")

def add_post(request):
  print(request.POST)
  PostImageFormset = inlineformset_factory(Account, Post, form = PostForm, extra=1)
  account = Account.objects.get(user = request.user)
  formset = PostImageFormset(queryset = Post.objects.none(), instance = account)
  # initial_dict = {
  #       "user_id" : account,
  #   }
  post_form = PostForm()
  
  if request.method == 'POST':
    post_form = PostForm(request.POST, request.FILES)
    if post_form.is_valid():
      obj = post_form.save(commit = False)
      obj.user_id = account
      print(post_form.cleaned_data)
      obj.save()
      # formset.save(commit=False)
    else:
      print("not_saved")
  return redirect('home')

def add_comment(request, id):
  post = Post.objects.get(id = id)
  form = CommentForm()
  if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
      obj = form.save(commit = False)
      obj.post_id = post
      obj.user_id = request.user.account
      obj.save()
      
  context = {
    "form": form,
  }
  return redirect('home')

def add_followee(request, id):
  print("followee entered")
  follower = Account.objects.get(user = request.user)
  followee = Account.objects.get(id = id)
  Follower.objects.create(follower_id = follower, followee_id = followee)

  return redirect('home')
