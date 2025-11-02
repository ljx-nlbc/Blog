from django.urls import path,include
from . import views

app_name = "blog"
urlpatterns=[
    #普通视图url：
    #path('',views.ArticleListView,name='article_list'),
    path('article/<int:article_id>',views.ArticleDetailView,name='article_detail'),
    path('article/create/',views.ArticleCreateView,name='article_create'),
    path('article/<int:article_id>/update/',views.ArticleUpdateView,name='article_update'),


    #通用视图url：
    path('',views.ArticleListView.as_view(),name='article_list'),
    #path('article/<int:pk>',views.ArticleDetailView.as_view(),name='article_detail'),  
    #path('article/create/',views.ArticleCreateView.as_view(),name='article_create'), 
    # path('article/<int:pk>/update/',views.ArticleUpdateView.as_view(),name='article_update'),
    path('article/<int:pk>/delete/',views.ArticleDeleteView.as_view(),name='atricle_delete'),
    path('category/<int:category_id>/',views.category_articles,name='category_articles'),
    path('article/comment/<int:article_id>/',views.add_comment,name='add_comment'),
    path('user/<int:user_id>-<str:username>/',views.user_profile,name = 'user_profile'),
]
