from django import forms
class LoginForm(forms.Form):
    password=forms.PasswordInput()
    username=forms.CharField(max_length=16,min_length=8,label='请输入用户名')
