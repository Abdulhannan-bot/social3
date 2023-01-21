from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from foundation_filefield_widget.widgets import FoundationFileInput, FoundationImageInput
from django.core.files import File
from PIL import Image

from .models import *

class SignUpForm(UserCreationForm):
  username = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  first_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  last_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, widget = forms.EmailInput(attrs = {'class': "form-control"}))
  password1 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))
  password2 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AccountForm(ModelForm):
  full_name = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  profile_pic = forms.ImageField(widget = forms.FileInput(attrs = {'class': "form-control"}))
  class Meta:
    model = Account
    fields = ['full_name', 'email', 'profile_pic']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ['created_at']

class SearchForm(ModelForm):
  username = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
    
class PostForm(ModelForm):
  x = forms.FloatField(widget=forms.HiddenInput(), required=False)
  y = forms.FloatField(widget=forms.HiddenInput(), required=False)
  width = forms.FloatField(widget=forms.HiddenInput(), required=False)
  height = forms.FloatField(widget=forms.HiddenInput(), required=False)
  description = forms.CharField(widget = forms.TextInput(attrs = {'class': "form-control", 'placeholder': 'Write something ...'}), required=False),

  class Meta:
    model = Post
    fields = ['File', 'description', 'x', 'y', 'width', 'height', ]
    # widgets = {
    #   'File': FoundationFileInput(attrs = {'class': "form-control"}, renderer=None),
    # }
  
  def save(self, *args, **kwargs):
    post = super(PostForm, self).save()
    if post.File:
      
      x = self.cleaned_data.get('x')
      y = self.cleaned_data.get('y')
      w = self.cleaned_data.get('width')
      h = self.cleaned_data.get('height')

      if(x and y and w and h):

        image = Image.open(post.File)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(post.File.path)

    return post