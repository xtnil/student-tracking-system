from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .decorator import *
from django.core.exceptions import PermissionDenied
from datetime import datetime
from datetime import date

# Create your views here.



def index(request):
    return render(request,'common/index.html')



@OnlyAuth
def signin(request):
    LM = LoginForm(request.POST or None)
    if request.method == 'POST':
        if LM.is_valid():
            UserName = request.POST.get('username')
            PassWord = request.POST.get('password')
            user = authenticate(request, username=UserName, password=PassWord)

            if user is not None and user.is_cdc:
                login(request, user)
                return redirect('cdc')
            elif user is not None and user.is_teacher:
                login(request, user)
                return redirect('teacher')
            elif user is not None and user.is_student:
                login(request, user)
                return redirect('student')
            else:
                messages.error(request, 'Username or Password is incorrect')
        else:
            messages.error(request, LM.errors)
    else:
        LM = LoginForm()
    context = {'form': LM}
    return render(request, 'common/signin.html', context)


@OnlyAuth
def signup(request):
    if request.method == 'POST':
        SF = SignupForm(request.POST)
        if SF.is_valid():
            isStudent = SF.cleaned_data.get('is_student')
            isTeacher = SF.cleaned_data.get('is_teacher')
            if isStudent:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_student = True
                SignUpUser.status = True
                SignUpUser.save()
            elif isTeacher:
                SignUpUser = SF.save(commit=False)
                SignUpUser.is_teacher = True
                SignUpUser.status = False
                SignUpUser.save()
            else:
                messages.warning(request, 'Please Select Your user Type')
                return redirect('signin')
            user = SF.cleaned_data.get('username')
            messages.success(request, 'Account Created for ' + user)
            return redirect('signin')
        else:
            messages.error(request, SF.errors)
    else:
        SF = SignupForm()
    context = {'form': SF}
    return render(request, 'common/signup.html', context)


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def student(request):
    if not request.user.is_student:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_student = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'student/StudentProfile.html', context)


@login_required(login_url='signin')
def activity(request):
    if not request.user.is_student:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    Activitydata = Activity.objects.filter(activityowner=request.user.id)
    if request.method == 'POST':
        ActivityProfileForm = ActivityProfile(request.POST, request.FILES)
        if ActivityProfileForm.is_valid():
            studentActivity = ActivityProfileForm.save(commit=False)
            studentActivity.status = False
            studentActivity.activityowner = request.user.id
            studentActivity.save()
            messages.success(
                request, 'Your Activity Details is submited and wait for CDC process')
        else:
            messages.warning(request, ActivityProfileForm.errors)
    else:
        ActivityProfileForm = ActivityProfile()

    context = {'StudentData': userdata, 'Activitydata': Activitydata,
               'ActivityProfileForm': ActivityProfileForm}
    return render(request, 'student/Activity.html', context)


@login_required(login_url='signin')
def academic(request):
    return render(request, 'student/Activity.html')


@login_required(login_url='signin')
def cdc(request):
    if not request.user.is_cdc:
        raise PermissionDenied
    return render(request, 'admin/CdcProfile.html')


@login_required(login_url='signin')
def category(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    categorydata = QuestionCategory.objects.filter(owner=request.user.id)
    if request.method == 'POST':
        CategoryForm = CategoryManagement(request.POST)
        if CategoryForm.is_valid():
            CF = CategoryForm.save(commit=False)
            CF.status = True
            CF.owner = request.user.id
            CF.save()
            messages.success(
                request, 'Your Category Details is submited and wait for CDC process')
        else:
            messages.warning(request, CategoryForm.errors)
    else:
        CategoryForm = CategoryManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'CategoryForm': CategoryForm}
    return render(request, 'Quora/Category.html', context)


@login_required(login_url='signin')
def addquestion(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    categorydata = QuestionCategory.objects.all()
    userdata = User.objects.get(pk=request.user.id)
    questiondata = Question.objects.filter(owner=request.user.id)

    if request.method == 'POST':
        QuestionForm = QuestionManagement(request.POST, request.FILES)
        print(QuestionForm)
        if QuestionForm.is_valid():
            QF = QuestionForm.save(commit=False)
            QF.status = False
            QF.owner = request.user.id
            QF.postedtime = date.today()
            QF.save()
            messages.success(
                request, 'Your Question  is submited and wait for CDC Approvel')
        else:
            messages.warning(request, QuestionForm.errors)
    else:
        QuestionForm = QuestionManagement()

    context = {'StudentData': userdata, 'categorydata': categorydata,
               'QuestionForm': QuestionForm, 'questiondata': questiondata}
    return render(request, 'Quora/AddQuestion.html', context)


@login_required(login_url='signin')
def allquestion(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    try:
        questiondata = Question.objects.all()
    except Question.DoesNotExist:
        questiondata = None

    AllQuestion = []
    if questiondata is not None:
        for QD in questiondata:
            user = User.objects.get(pk=QD.owner)
            category = QuestionCategory.objects.get(pk=QD.questioncategory)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            if category is not None:
                catname = category.name
            else:
                catname = ""

            AllQuestion.append({
                "id": QD.id,
                "question": QD.question,
                "questioncategory": QD.questioncategory,
                'categoryname': catname,
                'owner': QD.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": QD.postedtime,
            })

    context = {'StudentData': userdata, 'questiondata': AllQuestion}
    return render(request, 'Quora/AllQuestions.html', context)


@login_required(login_url='signin')
def addnews(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)

    try:
        newsdetails = News.objects.all()
    except News.DoesNotExist:
        newsdetails = None

    AllNews = []
    if newsdetails is not None:
        for ND in newsdetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            AllNews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime,
            })
            print(AllNews)

    if request.method == 'POST':
        NewsForm = NewsManagement(request.POST, request.FILES)
        if NewsForm.is_valid():
            news = NewsForm.save(commit=False)
            news.status = False
            news.owner = request.user.id
            news.postedtime = date.today()
            news.save()
            messages.success(
                request, 'Your News Details is submited and wait for CDC process')
        else:
            messages.warning(request, NewsForm.errors)
    else:
        NewsForm = NewsManagement()

    context = {'StudentData': userdata, 'NewsData': newsdetails,
               'NewsForm': NewsForm}
    return render(request, 'news/addnews.html', context)


@login_required(login_url='signin')
def allnews(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    try:
        newsdetails = News.objects.all()
    except News.DoesNotExist:
        newsdetails = None

    AllNews = []
    if newsdetails is not None:
        for ND in newsdetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            AllNews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime
            })
    context = {'StudentData': userdata, 'NewsData': newsdetails}
    return render(request, 'news/Allnews.html', context)


@login_required(login_url='signin')
def addpin(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)

    try:
        newsdetails = News.objects.all()
    except News.DoesNotExist:
        newsdetails = None

    AllNews = []
    if newsdetails is not None:
        for ND in newsdetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            AllNews.append({
                "id": ND.id,
                "headlines": ND.headlines,
                "details": ND.details,
                'dept': ND.dept,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime,
            })

    if request.method == 'POST':
        PinForm = PinManagement(request.POST, request.FILES)
        if PinForm.is_valid():
            pin = PinForm.save(commit=False)
            pin.status = True
            pin.owner = request.user.id
            pin.postedtime = date.today()
            pin.save()
            messages.success(
                request, 'Your News Pin is submited and wait for CDC process')
        else:
            messages.warning(request, PinForm.errors)
    else:
        PinForm = PinManagement()
    context = {'StudentData': userdata,
               'NewsData': newsdetails, 'PinForm': PinForm}
    return render(request, 'pin/addpin.html', context)


@login_required(login_url='signin')
def allpin(request):
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)

    try:
        pindetails = Pin.objects.all()
    except Pin.DoesNotExist:
        pindetails = None

    pinNews = []
    if pindetails is not None:
        for ND in pindetails:
            user = User.objects.get(pk=ND.owner)
            if user is not None:
                author = user.first_name + ' ' + user.last_name
                img = user.profilepic.url
            else:
                author = ""

            pinNews.append({
                "id": ND.id,
                "heading": ND.heading,
                "details": ND.details,
                'dept': ND.pincategory,
                'tag': ND.tag,
                'owner': ND.owner,
                'ownername': author,
                'ownerimg': img,
                "postedtime": ND.postedtime,
                'pin': ND.pin
            })
    context = {'StudentData': userdata, 'pinNews': pinNews}
    return render(request, 'pin/Allpin.html', context)


@login_required(login_url='signin')
def teacher(request):
    if not request.user.is_teacher:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        UserProfileForm = SignupForm(
            request.POST, request.FILES, instance=userdata)

        if UserProfileForm.is_valid():
            student = UserProfileForm.save(commit=False)
            student.is_teacher = True
            student.status = True
            UserProfileForm.save()
            messages.success(
                request, 'Profile is Updated. please login again to craete a new Session')
            return redirect('signout')
        else:
            messages.warning(request, UserProfileForm.errors)
    else:
        UserProfileForm = SignupForm(instance=userdata)
    context = {'StudentData': userdata, 'UserProfileForm': UserProfileForm}
    return render(request, 'teacher/TeacherProfile.html', context)


def allstudent(request):
    if not request.user.is_teacher:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')

    userdata = User.objects.get(pk=request.user.id)
    studentdata = User.objects.all()
    allstudent = []

    for i in studentdata:
        if i.is_student == True:
            allstudent.append({
                "id": i.id,
                "first_name": i.first_name,
                "last_name": i.last_name,
                'dept': i.dept,
                'year': i.year,
                'semester': i.semester,
                'enrollment': i.enrollment,
                'profilepic': i.profilepic,
            })

    context = {'StudentData': userdata, 'allstudent': allstudent}
    return render(request, 'teacher/allstudent.html', context)

#for teacher only
def addacademic(request, pk):
    if not request.user.is_teacher:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    studentdetails = User.objects.get(pk=pk)
    StudentMarks=Academic.objects.filter(Student=pk)
    
    if request.method == 'POST':
        AcademicForm = AcademicProfile(request.POST)
        if AcademicForm.is_valid():
            AcademicUser = AcademicForm.save(commit=False)
            AcademicUser.Student = pk
            AcademicUser.Treacher = request.user.id
            AcademicUser.studentenrollment = studentdetails.enrollment
            AcademicUser.date=date.today()
            AcademicUser.save()
            messages.success(
                request, 'Marks & Attendence is Saved')
            return redirect('allstudent')
        else:
            messages.warning(request, AcademicForm.errors)
    else:
        AcademicForm = AcademicProfile()
    context = {'StudentData': userdata, 'AcademicForm': AcademicForm,'studentdetails':studentdetails,'StudentMarks':StudentMarks}
    return render(request, 'teacher/Academic.html', context)


#for student only
def viewacademic(request):
    if not request.user.is_student:
        raise PermissionDenied
    if not request.user.status:
        return render(request, 'common/notActive.html')
    userdata = User.objects.get(pk=request.user.id)
    StudentMarks=Academic.objects.filter(Student=request.user.id)
    context = {'StudentData': userdata,'StudentMarks':StudentMarks}
    return render(request, 'student/Academic.html', context)
    
