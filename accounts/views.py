from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        #显示空的注册表单
        form = UserCreationForm()
    else:
        #处理填写好的表单
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #让用户自动登陆,再重定向到主页
            login(request,new_user)
            return redirect('blog:article_list')
    context = {'form':form}
    return render(request,'registration/register.html',context)



