from django.contrib import admin
from .models import Article


# модель отображения в админке
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')  # отображать на главное
    list_filter = ("status",)  # фильтр
    search_fields = ['title', 'content']  # фильтрация поиска
    prepopulated_fields = {'slug': ('title',)}  # генерация ссылки по названию заголовка


admin.site.register(Article, ArticleAdmin)
