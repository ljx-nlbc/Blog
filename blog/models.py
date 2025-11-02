from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类',max_length=100,default='category')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        #在admin后台显示
        verbose_name = '分类'#单数显示
        verbose_name_plural = verbose_name#复数显示                                                              

    def __str__(self):
        return self.name

    
class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签',max_length=100,default='tag')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
class Article(models.Model):
    """博客文章"""
    title = models.CharField('标题',max_length=200)
    content = models.TextField('内容')
    excerpt = models.CharField('摘要',max_length=200,blank=True)

    #关系字段
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='作者'
                               )
    category = models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='分类')
    tags = models.ManyToManyField(Tag,blank=True,verbose_name='标签')

    #时间字段
    created = models.DateTimeField('创建时间',auto_now_add=True)
    updated = models.DateTimeField('更新时间',auto_now=True)

    #游览量字段
    views = models.PositiveIntegerField('游览量',default=0)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created']#按照创建时间倒叙排列
    
    #这个函数在views = article.increase_views()会使用到
    # def increase_views(self):
    #     """增加游览量"""
    #     self.views += 1
    #     #只保存单个字段，如果只写self.save()那么保存的是所有字段
    #     self.save(update_fields=['views'])

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    """文章评论"""
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='文章')
    usr = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    content=models.TextField('评论内容')
    created = models.DateTimeField('创建时间',auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return f'{self.usr.username}:{self.content[:20]}'    


