from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Article


# форма для регистрации
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # делаем поле email обязательным

    class Meta:
        model = User  # указываем модель  юзера
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )  # поля которые будут отображаться

    def save(self, commit=True):  # функция сохранения
        user = super(RegistrationForm, self).save(commit=False)  # создаем юзера
        user.first_name = self.cleaned_data['first_name']  # вписываем имя
        user.last_name = self.cleaned_data['last_name']  # вписываем фамилию
        user.email = self.cleaned_data['email']  # вписываем email

        if commit:
            user.save()  # сохраняем

        return user


# форма изменения личных данных
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )


# форма создания статьи
class ArticleForm(forms.ModelForm):
    STATUS_CHOICE = (
        (0, "Draft"),
        (1, "Publish")
    )
    title = forms.CharField(required=True)  # поле заголовок
    status = forms.ChoiceField(choices=STATUS_CHOICE, required=True)  # поле статуса
    content = forms.CharField(required=True, widget=forms.Textarea())  # поле текста

    class Meta:
        model = Article
        fields = (
            'title',
            'content',
            'status'
        )
