from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'email', 'dept', 'year', 'semester',
                    'enrollment', 'profilepic',
                    'is_cdc', 'is_teacher', 'is_student', 'status']


@admin.register(Academic)
class AcademicAdmin(admin.ModelAdmin):
    list_display = ['id', 'Student', 'Treacher', 'studentenrollment', 'studentdept',
                    'studentyear', 'studentsemester', 'subject', 'subjectattendence', 'subjectclass', 'subjectscore', 'subjectmarks', 'date']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'activityname', 'activitydetails', 'activitydate',
                    'activityowner', 'status']


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'status']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'questioncategory',
                    'owner', 'status', 'postedtime']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'questionid',
                    'solver', 'answertime', 'status']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'headlines', 'details',
                    'dept', 'owner', 'status', 'postedtime']


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ['id', 'pin', 'heading',
                    'tag', 'details', 'owner', 'pincategory', 'status', 'postedtime']
