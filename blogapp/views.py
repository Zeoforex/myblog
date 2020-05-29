from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, RegistrationForm, ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth import login


# главная страница
def article_list(request):
    if request.GET.get('q') and request.method == 'GET':  # если есть параметры для поиска
        article_list = get_article_queryset(request.GET.get('q'))  # делаем поиск
    else:  # если нет параметров на поиск
        article_list = Article.objects.filter(status=1).order_by(
            '-created_on')  # получаем все опубликованные статьи и сортируем
    # разбиваем список статей на страницы
    page = request.GET.get('page', 1)
    paginator = Paginator(article_list, 10)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'articles': articles})


# страница статьи
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)  # получаем статью либо 404
    context = {'article': article}
    return render(request, 'article_detail.html', context=context)


# поиск по заголовкам и тексту статей
def get_article_queryset(query=None):
    queryset = []  # ключевые слова
    queries = query.split(' ')  # разбиваем строку поиска на слова
    for q in queries:  # для каждого ключевого слова в списке слов
        articles = Article.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).distinct()  # поиск ключевого слова по тексту и заголовкам

        for article in articles:  # добавляем каждую найденную статью в список
            queryset.append(article)

    return list(set(queryset))  # возвращаем список статей


# страница мой профиль
@login_required()  # только для авторизированных
def myprofile(request):
    if request.method == "POST":  # если есть POST запрос на сохранение формы
        form = EditProfileForm(request.POST, instance=request.user)  # заполняем форму

        if form.is_valid():  # если все корректно
            form.save()  # сохраняем изменения
            return redirect('/myprofile')
    else:  # если просто загружаем страницу
        form = EditProfileForm(instance=request.user)  # передаем форму для изменения личных данных пользователя
        context = {'form': form}
        return render(request, 'myprofile.html', context=context)


# страница мои статьи
@login_required()
def myarticles(request):
    article_list = Article.objects.filter(author=request.user).order_by(
        '-created_on')  # получаем все статьи пользователя

    # разбиваем список статей на страницы
    page = request.GET.get('page', 1)
    paginator = Paginator(article_list, 10)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'myarticles.html', {'articles': articles})


# страница со списком авторов
def author_list(request):
    authors_list = User.objects.filter()  # получаем список всех авторов
    # разбиваем список на страницы
    page = request.GET.get('page', 1)
    paginator = Paginator(authors_list, 10)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, 'authors.html', {'authors': authors})


# страница конкретного автора
def author_detail(request, username):
    author = get_object_or_404(User, username=username)  # ищем нужного автора либо 404
    article_list = Article.objects.filter(status=1, author=author).order_by(
        '-created_on')  # получаем все опубликованные статьи нужного автора
    # разбиваем список статей на страницы
    page = request.GET.get('page', 1)
    paginator = Paginator(article_list, 10)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request, 'author_detail.html', {'articles': articles, 'author': author})


# удаление статьи
@login_required()
def delete_article(request, title):
    article = Article.objects.get(title=title)  # находим статью с нужным заголовком
    if request.user == article.author:  # если юзер который послал запрос на удаление является автором статьи
        article.delete()  # удаляем статью
    return redirect('/myarticles')


# скрыть/показать статью
@login_required()
def show_article(request, title):
    article = Article.objects.get(title=title)  # находим статью с нужным заголовком
    if request.user == article.author:  # если юзер который послал запрос является автором статьи
        if article.status == 0:  # если статья скрыта
            article.status = 1  # делаем ее опубликованной
        else:  # если наоборот
            article.status = 0  # то делаем ее скрытой
        article.save()  # сохраняем изменения
    return redirect('/myarticles')


# страница с регистрацией
def registration(request):
    if request.user.is_authenticated:  # если юзер уже авторизован то перебрасываем его на главную страницу
        return redirect('/')

    if request.method == "POST":  # если есть запрос на регистрацию
        form = RegistrationForm(request.POST)  # форма регистрации
        if form.is_valid():  # если данные корректны
            user = form.save()  # сохраняем юзера
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # логиним юзера
            return redirect('/myprofile')  # перенаправляем на страницу мой профиль

    form = RegistrationForm()  # форма регистрации
    context = {'form': form, 'errors': form.errors}
    return render(request, 'registration/registration.html', context=context)


# страница создания статьи
@login_required()
def create_article(request):
    if request.method == "POST":  # если есть запрос на создание
        form = ArticleForm(request.POST)
        if form.is_valid():  # если данные корректны
            article = form.save(commit=False)  # создаем запись в бд но не сохраняем
            article.author = request.user  # вписываем юзера как автора
            article.save()  # сохраняем
            return redirect('/myarticles')

    context = {'form': ArticleForm}
    return render(request, 'create_article.html', context=context)