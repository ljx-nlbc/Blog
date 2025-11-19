from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.core.paginator import Paginator

from .models import Article,Tag,Category,Comment
from .forms import ArticleForm,CommentForm


# class ArticleListView(generic.ListView):
#     """文章列表视图(通用视图)"""
#     model = Article
#     template_name = 'blog/article_list.html'
#     context_object_name = "articles"
#     paginate_by = 1

#     def get_queryset(self):
#         #这是通用视图的方法，对该方法进行了重写:预加载外键关系，减少查询次数
#         return Article.objects.all().select_related('author','category')
    
    
def ArticleListView(request):
    """文章列表视图"""
    articles = Article.objects.all().order_by('-created')
    paginator = Paginator(articles,5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    elided_page_range = paginator.get_elided_page_range(page_obj.number,
                                                        on_each_side=2,
                                                        on_ends=1)
    context = {"articles":articles,"page_obj":page_obj,'elided_page_range':elided_page_range,'request': request}
    return render(request,'blog/article_list.html',context)


# class ArticleDetailView(generic.DetailView):
#     """文章详情页(通用视图)只有GET方法"""
#     model = Article
#     template_name = 'blog/article_detail.html'
#     context_object_name = 'article'

#     def get_object(self):
#         """获取文章对象并增加浏览量"""
#         obj = super().get_object()
#         obj.increase_views()
#         return obj

def ArticleDetailView(request,article_id):
    """文章详情页"""
    article = Article.objects.get(id=article_id)
    #views = article.increase_views()
    views = Article.objects.filter(pk=article_id).update(views=F('views')+1)
    comment_form = CommentForm()
    #删除文章
    if request.method == 'POST':
        if 'delete_article' in request.POST:
            if request.user != article.author:
                messages.error(request,'你不能进行文章删除！')
                return redirect('blog:article_list')
            article.delete()
            messages.success(request,'文章已删除!')
            return redirect('accounts:homepage',user_id=request.user.id,username=article.author)
        elif 'submit_comment' in request.POST:    
            add_comment(request,article)         
            return redirect('blog:article_detail',article_id=article_id)
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            if comment_id:
                delete_comment(request,comment_id)
            return redirect('blog:article_detail',article_id=article_id)
    context = {'article':article,'views':views,"comment_form":comment_form}
    return render(request,'blog/article_detail.html',context)

@login_required
def add_comment(request,article):
    """添加评论"""
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.usr = request.user
        comment.save()

@login_required
def delete_comment(request,comment_id=None):
    if comment_id is None:
        comment_id = request.POST.get('comment_id')
    if not comment_id:
        messages.error(request,'未指定要删除的评论')
        return
    
    comment = Comment.objects.filter(id=comment_id).first()
    if not comment:
        messages.error(request,'评论不存在')
        return 
    
    if request.user == comment.usr:
        comment.delete()
    else:
        messages.error(request,'你没有权限删除该评论')
    

# class ArticleCreateView(LoginRequiredMixin,generic.CreateView):
#     """创建新文章"""
#     model = Article
#     template_name = 'blog/article_form.html'
#     form_class = ArticleForm

#     def form_valid(self, form):
#         #在保存表单前设置作者为当前用户
#         form.instance.author = self.request.user
#         messages.success(self.request,'文章发布成功！')
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         """文章创建成功的行为"""
#         #将界面重定向到用户首页
#         return reverse_lazy('blog:user_profile', kwargs={
#             'user_id': self.request.user.id,
#             'username': self.request.user.username}
#             )
    
def ArticleCreateView(request):
    """创建新文章"""
    if request.method != 'POST':
        form = ArticleForm()
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            #获取表单实例但是不立即保存到数据库
            article = form.save(commit=False)
            #设置当前用户为作者
            article.author = request.user
            form.save()
            #redirect通常用在函数中，返回的是Httpxxx响应
            return redirect('blog:article_detail',article_id=article.id)
    context = {'form':form}
    return render(request,'blog/article_form.html',context)
    
class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
    """更新文章"""
    model = Article
    template_name = 'blog/article_form.html'
    form_class = ArticleForm

    def form_valid(self, form):
        #在保存表单前设置作者为当前用户
        form.instance.author = self.request.user
        messages.success(self.request,'文章更新成功！')       
        return super().form_valid(form)

    def get_success_url(self):
        """文章更新成功的行为"""
        messages.success(self.request, '文章更新成功！')
        #将界面重定向到用户首页reverse_lazy延迟解析，通常在类属性中，返回的是解析出的url字符串
        return reverse_lazy('blog:user_profile', kwargs={
            'user_id': self.request.user.id,
            'username': self.request.user.username}
            )
    
def ArticleUpdateView(request,article_id):
    """更新文章"""
    article = Article.objects.get(id=article_id)
    if request.method != 'POST':
        article_update = ArticleForm(instance=article)
    else:
        article_update = ArticleForm(instance=article,data=request.POST)
        if article_update.is_valid():
            #获取表单实例但是不立即保存到数据库
            article = article_update.save(commit=False)
            #设置当前用户为作者
            article.author = request.user
            article_update.save()
            return redirect('accounts:homepage',user_id=request.user.id,username=article.author)
    context = {'form':article_update}
    return render(request,'blog/article_form.html',context)


class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    """删除视图"""
    model = Article
    template_name = 'blog/article_detail.html'
    #success_url = 'blog/article_list.html'
    
    def test_func(self):
        """确保只有文章作者可以删除"""
        article = self.get_object()
        return article.author == self.request.user
    
    def delete(self, request, *args, **kwargs):
        """重写delete方法以添加消息"""
        messages.success(self.request, '文章删除成功！')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """文删除成功的行为"""
        #将界面重定向到用户首页reverse_lazy延迟解析，通常在类属性中，返回的是解析出的url字符串
        return reverse_lazy('accounts:homepage', kwargs={
            'user_id': self.request.user.id,
            'username': self.request.user.username}
            )

def category_articles(request,category_id):
    """文章分类列表"""
    category = get_object_or_404(Category,pk=category_id)
    articles = Article.objects.filter(category=category).select_related('author','category')

    context={
        'category':category,
        'articles':articles,
    }
    return render(request,'blog/category_articles.html',context)