from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


# модель статьи в бд
class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)  # заголовок
    slug = models.SlugField(max_length=200, unique=True)  # ссылка
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # автор
    updated_on = models.DateTimeField(auto_now=True)  # дата обновления статьи
    content = models.TextField()  # контент статьи
    created_on = models.DateTimeField(auto_now_add=True)  # дата создания статьи
    status = models.IntegerField(choices=STATUS, default=0)  # статус статьи

    class Meta:
        ordering = ['-created_on']  # сортировка по дате добавления

    def __str__(self):
        return self.title  # отображать название

    def save(self, *args, **kwargs):
        if not self.slug:  # если ссылка не прописана
            self.slug = slugify(self.title)  # генерируем ссылку по заголовку
        super(Article, self).save(*args, **kwargs)  # сохраняем
