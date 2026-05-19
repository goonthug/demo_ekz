from django.db import models


class User(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='E-mail')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.full_name


class Course(models.Model):
    TYPE_CHOICES = [
        ('qualification', 'Повышение квалификации'),
        ('retraining', 'Переподготовка'),
        ('safety', 'Охрана труда'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название курса')
    course_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип курса')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Идет обучение'),
        ('completed', 'Обучение завершено'),
    ]

    PAYMENT_CHOICES = [
        ('card', 'Банковская карта'),
        ('transfer', 'Банковский перевод'),
        ('cash', 'Наличные'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    start_date = models.DateField(verbose_name='Дата начала')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.full_name} — {self.course.name}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f'Отзыв от {self.user.full_name}'
