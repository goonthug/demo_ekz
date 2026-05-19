import re
from django import forms
from .models import User, Application, Review


class RegisterForm(forms.Form):
    login = forms.CharField(
        max_length=50,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    full_name = forms.CharField(
        max_length=200,
        label='ФИО',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов Иван Иванович'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )

    def clean_login(self):
        login = self.cleaned_data['login']
        if len(login) < 6:
            raise forms.ValidationError('Логин должен содержать минимум 6 символов')
        if not re.match(r'^[a-zA-Z0-9]+$', login):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры')
        if User.objects.filter(login=login).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        return password


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=50,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    password = forms.CharField(
        max_length=128,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )


class ApplicationForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=None,
        label='Курс',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    start_date = forms.DateField(
        label='Дата начала',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(
        choices=[('card', 'Банковская карта'), ('transfer', 'Банковский перевод'), ('cash', 'Наличные')],
        label='Способ оплаты',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Course
        self.fields['course'].queryset = Course.objects.all()


class ReviewForm(forms.Form):
    text = forms.CharField(
        label='Отзыв',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Напишите ваш отзыв...'})
    )
