
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название курса')),
                ('course_type', models.CharField(choices=[('qualification', 'Повышение квалификации'), ('retraining', 'Переподготовка'), ('safety', 'Охрана труда')], max_length=20, verbose_name='Тип курса')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('payment_method', models.CharField(choices=[('card', 'Банковская карта'), ('transfer', 'Банковский перевод'), ('cash', 'Наличные')], max_length=20, verbose_name='Способ оплаты')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('in_progress', 'Идет обучение'), ('completed', 'Обучение завершено')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course', verbose_name='Курс')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user', verbose_name='Пользователь')),
            ],
            options={
                'db_table': 'applications',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.application', verbose_name='Заявка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user', verbose_name='Пользователь')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
    ]
