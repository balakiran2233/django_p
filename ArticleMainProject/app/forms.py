from django import forms
from .models import Post,Profile,CommentData
from django.contrib.auth.models import User


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body']

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','body']

class commentform(forms.ModelForm):
    class Meta:
        model = CommentData
        fields = ['comment']





class UserLoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label="", widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        else:
            return confirm_password
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
