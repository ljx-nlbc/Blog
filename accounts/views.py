from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404

from .forms import AvatarUpdateForm
from .models import Profile
from blog.models import Article

def register(request):
    """注册新用户"""
    if request.method != 'POST':
        #显示空的注册表单和头像表单
        registerform = UserCreationForm()
        profileform = AvatarUpdateForm()
    else:
        registerform = UserCreationForm(data=request.POST)
        # profileform = AvatarUpdateForm(request.POST, request.FILES)
        if registerform.is_valid():
            # 如果两个表单都有效，再保存
            # if profileform.is_valid():
            # 保存用户
            new_user = registerform.save()
            # 创建或获取 Profile
            profile, created = Profile.objects.get_or_create(user=new_user)
            profileform = AvatarUpdateForm(request.POST, request.FILES,instance=profile)
            # if 'avatar' in request.FILES:
            #     profile.avatar = request.FILES['avatar']
            # if 'bio' in request.POST:
            #     profile.bio = request.POST['bio']
            # profile.save()
            if profileform.is_valid():
                profileform.save()        
                messages.success(request, '注册成功！')
                login(request, new_user)
                # print("注册用户的头像地址：", new_user.profile.avatar.url)
                return redirect('blog:article_list')
            else:
                # 头像表单无效，但仍然创建用户（使用默认头像）
                new_user = registerform.save()
                messages.success(request, '注册成功！但头像上传失败，请稍后修改。')
                login(request, new_user)
                return redirect('blog:article_list')
        else:
            # 用户表单无效
            messages.error(request, '注册失败！')
    
    context = {'registerform': registerform, "profileform": profileform}
    return render(request, 'registration/register.html', context)

@login_required
def homepage(request,user_id,username):
    """用户主页"""
    #首先检查当前登陆用户是否与url中的用户匹配
    if request.user.id != int(user_id) or request.user.username != username:
        return redirect('accounts:login')

    user = get_object_or_404(User,id=user_id,username=username)
    #将不是登陆用户写的文章过滤掉
    articles = Article.objects.filter(author=user)  
    profile,created = Profile.objects.get_or_create(user=request.user)
    #更改个人资料
    if request.method != 'POST':
        form = AvatarUpdateForm(instance=profile)     
    else:
        form = AvatarUpdateForm(
            request.POST, 
            request.FILES, 
            instance=profile
        )
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料已更新！')
            return redirect('accounts:homepage',user_id=request.user.id,username=user)        
    context = {'profileform': form,'articles':articles,'user':user}
    return render(request, 'accounts/homepage.html', context)

