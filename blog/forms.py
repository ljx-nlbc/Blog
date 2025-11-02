from django import forms
from .models import Article,Comment
class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields = ['category','tags','title','excerpt','content']
        labels = {
            'category':'分类',
            'tags':'标签',
            'title':'标题',
            'excerpt':'摘要',
            'content':'内容',
            }
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags':forms.CheckboxSelectMultiple(),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入文章标题'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '请输入文章摘要（可选）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '请输入文章内容'
            }),  
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 检查是否有分类数据
        if self.fields['category'].queryset.exists():
            self.fields['category'].empty_label = None
            self.fields['category'].initial = self.fields['category'].queryset.first()
        else:
            # 如果没有分类数据，显示提示信息
            self.fields['category'].empty_label = "暂无分类，请先创建分类"

class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content':forms.Textarea(attrs={
                'class':'form-control',
                'rows':1,
                'planceholder':'请输入评论内容...'
            })
        }