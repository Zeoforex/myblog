from . import views
from django.urls import path

urlpatterns = [
    path('', views.article_list, name='home'),
    path('registration/', views.registration, name='registration'), # страница регистрации
    path('create-article/', views.create_article, name='create_article'), # страница создания статьи
    path('myprofile/', views.myprofile, name='myprofile'), # страница мой профиль
    path('myarticles/', views.myarticles, name='myarticles'), # страница мои статьи
    path('delete-article/<str:title>', views.delete_article, name='delete_article'), # ссылка для удаления статьи передает параметр title
    path('show-article/<str:title>', views.show_article, name='show_article'), # ссылка для скрытия/показывания статьи передает параметр title
    path('author/', views.author_list, name='all_authors'), # страница списка авторов
    path('author/<str:username>', views.author_detail, name='author_detail'), # страница с конкретным автором передает параметр username
    path('<slug:slug>/', views.article_detail, name='article_detail'), # страница конкретной статьи передает параметр slug
]