from django.contrib import admin
from .models import User, Course, Application, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'full_name', 'phone', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_type')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'start_date', 'status')
    list_filter = ('status', 'course__course_type')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'created_at')
