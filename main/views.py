import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Course, Application, Review
from .forms import RegisterForm, LoginForm, ApplicationForm, ReviewForm


def register(request):
    if request.session.get('user_id'):
        return redirect('cabinet')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create(
                login=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
            )
            messages.success(request, 'Регистрация прошла успешно! Войдите в систему.')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.session.get('is_admin'):
        return redirect('admin_panel')
    if request.session.get('user_id'):
        return redirect('cabinet')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']

            if login == 'Admin26' and password == 'Demo20':
                request.session['is_admin'] = True
                request.session['admin_login'] = login
                return redirect('admin_panel')

            try:
                user = User.objects.get(login=login, password=password)
                request.session['user_id'] = user.id
                request.session['user_name'] = user.full_name
                return redirect('cabinet')
            except User.DoesNotExist:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('login')


def cabinet(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])
    applications = Application.objects.filter(user=user).select_related('course')
    reviews = Review.objects.filter(user=user).select_related('application')

    if request.method == 'POST' and 'review_text' in request.POST:
        app_id = request.POST.get('application_id')
        review_text = request.POST.get('review_text')
        try:
            app = Application.objects.get(id=app_id, user=user)
            if app.status == 'completed':
                Review.objects.create(user=user, application=app, text=review_text)
                messages.success(request, 'Отзыв добавлен!')
            else:
                messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        except Application.DoesNotExist:
            messages.error(request, 'Заявка не найдена')
        return redirect('cabinet')

    return render(request, 'main/cabinet.html', {
        'user': user,
        'applications': applications,
        'reviews': reviews,
    })


def apply(request):
    if not request.session.get('user_id'):
        return redirect('login')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            Application.objects.create(
                user_id=request.session['user_id'],
                course=form.cleaned_data['course'],
                start_date=form.cleaned_data['start_date'],
                payment_method=form.cleaned_data['payment_method'],
            )
            messages.success(request, 'Заявка успешно отправлена!')
            return redirect('cabinet')
    else:
        form = ApplicationForm()

    return render(request, 'main/apply.html', {'form': form})


def admin_panel(request):
    if not request.session.get('is_admin'):
        return redirect('login')

    applications = Application.objects.all().select_related('user', 'course')

    # Фильтр по статусу
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)

    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    applications = applications.order_by(sort_by)

    # Пагинация
    page = int(request.GET.get('page', 1))
    per_page = 10
    total = applications.count()
    total_pages = (total + per_page - 1) // per_page
    applications = applications[(page - 1) * per_page: page * per_page]

    # Изменение статуса
    if request.method == 'POST' and 'app_id' in request.POST and 'new_status' in request.POST:
        try:
            app = Application.objects.get(id=request.POST['app_id'])
            app.status = request.POST['new_status']
            app.save()
            messages.success(request, f'Статус заявки изменён на "{dict(Application.STATUS_CHOICES)[app.status]}"')
        except Application.DoesNotExist:
            messages.error(request, 'Заявка не найдена')
        return redirect('admin_panel')

    return render(request, 'main/admin_panel.html', {
        'applications': applications,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'page': page,
        'total_pages': total_pages,
        'total': total,
    })
