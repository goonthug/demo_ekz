import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')
django.setup()

from main.models import Course
courses = [
    ('Python-разработчик', 'qualification', 'Курс повышения квалификации по Python'),
    ('Менеджер проектов', 'retraining', 'Курс переподготовки по управлению проектами'),
    ('Охрана труда на производстве', 'safety', 'Курс по охране труда'),
    ('Веб-дизайн', 'qualification', 'Курс повышения квалификации по веб-дизайну'),
    ('1С:Предприятие', 'retraining', 'Курс переподготовки по 1С'),
    ('Пожарная безопасность', 'safety', 'Курс по пожарной безопасности'),
]
for name, ctype, desc in courses:
    Course.objects.get_or_create(name=name, defaults={'course_type': ctype, 'description': desc})
print('Курсы добавлены!')
