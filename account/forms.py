from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "User Name ..."
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Password..."
            })
    )


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "First Name..."
            }))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Last Name..."
            }))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "User Name..."
            }))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Email..."
            }))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Password..."
            }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': "Confirm Password..."
        }))
    dept = forms.CharField(
        widget=forms.Select(
            choices=DeptChoice,
            attrs={
                'class': 'form-control'
            }))
    year = forms.CharField(
        widget=forms.Select(
            choices=YearChoice,
            attrs={
                'class': 'form-control'
            }))
    semester = forms.CharField(
        widget=forms.Select(
            choices=SemChoice,
            attrs={
                'class': 'form-control'
            }))
    enrollment = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Enrollment Number.."
            }))

    profilepic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                # 'class': 'custom-file-input',
                'id': "customFile",
                'onchange': "readURL(this);",
                'style': "display: none;"
            }
        ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'dept', 'year', 'semester',
                  'enrollment', 'profilepic', 'status', 'is_cdc', 'is_teacher', 'is_student')


class AcademicProfile(forms.ModelForm):
    studentdept = forms.CharField(
        widget=forms.Select(
            choices=DeptChoice,
            attrs={
                'class': 'form-control'
            }))
    studentyear = forms.CharField(
        widget=forms.Select(
            choices=YearChoice,
            attrs={
                'class': 'form-control'
            }))
    studentsemester = forms.CharField(
        widget=forms.Select(
            choices=SemChoice,
            attrs={
                'class': 'form-control'
            }))

    subject = forms.CharField(
        widget=forms.Select(
            choices=SubjectChoice,
            attrs={
                'class': 'form-control'
            }))

    subjectattendence = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Total Attendes of Student.."
            }))
    subjectclass = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Total No of Classes.."
            }))
    subjectscore = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Score of Student..."
            }))
    subjectmarks = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Total Marks..."
            }))
    studentenrollment = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Enrollment Number.."
            }))

    class Meta:
        model = Academic
        fields = ('Student', 'Treacher', 'studentenrollment', 'studentdept',
                  'studentyear', 'studentsemester', 'subject', 'subjectattendence', 'subjectclass', 'subjectscore', 'subjectmarks', 'date')


class ActivityProfile(forms.ModelForm):
    activityname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Activity Name...."
            }))

    activitydate = forms.DateField(
        widget=DateInput(attrs={
            'class': 'form-control'
        }))

    activitydetails = forms.Textarea()

    class Meta:
        model = Activity
        fields = ('activityname', 'activitydetails', 'activitydate',
                  'activityowner', 'status')


class CategoryManagement(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Category Name..."
            }))

    class Meta:
        model = QuestionCategory
        fields = ('name', 'owner', 'status')


class QuestionManagement(forms.ModelForm):
    question = forms.Textarea()

    class Meta:
        model = Question
        fields = ('question', 'questioncategory',
                  'owner', 'status', 'postedtime')


class AnswerManagement(forms.ModelForm):
    answer = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': "Provide your Answer Hear..."
            }))

    class Meta:
        model = Answer
        fields = ('answer', 'questionid',
                  'solver', 'answertime', 'status')


class NewsManagement(forms.ModelForm):
    headlines = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "News Headline..."
            }))

    details = forms.Textarea()

    dept = forms.CharField(
        widget=forms.Select(
            choices=NewsDeptChoice,
            attrs={
                'class': 'form-control'
            }))

    class Meta:
        model = News
        fields = ('headlines', 'details', 'dept',
                  'owner', 'status', 'postedtime')


class PinManagement(forms.ModelForm):
    heading = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Pin Headline..."
            }))
    tag = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Tages....."
            }))
    # details = forms.Textarea(attrs={"rows": 5, "cols": 20})
    details = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 115}))

    pincategory = forms.CharField(
        widget=forms.Select(
            choices=Pincategory,
            attrs={
                'class': 'form-control'
            }))
    pin = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                # 'class': 'custom-file-input',
                'id': "customFile",
                'onchange': "readURL(this);",
                'style': "display: none;"
            }
        ))

    class Meta:
        model = Pin
        fields = ('pin', 'heading',
                  'tag', 'details', 'owner', 'pincategory', 'status', 'postedtime')
