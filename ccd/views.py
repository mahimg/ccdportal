from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.db.models import Q
import csv
import codecs
from datetime import datetime
from django.utils.timezone import utc

@login_required(login_url='ccd:login')
def index(request):
    if request.user.is_authenticated():
        context = {}
        allStudents = Student.objects.all().order_by('-lastUpdated')[:100]
        context['allStudents'] = allStudents
        updates = Update.objects.all().order_by('-addedOn')[:2]
        context['updates'] = updates
        return render(request, 'ccd/index.html', context)
    return HttpResponse("Not permitted to use this site")


def loginUser(request):
    if request.user.is_authenticated():
        return redirect('ccd:index')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            username = User.objects.get(email=username).username
        except Exception as e:
            pass
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'ccd/login.html', {'login_error_message': 'User Inactive. Contact Admin!'})
        else:
            return render(request, 'ccd/login.html', {'login_error_message': 'Invalid login credentials'})
    return render(request, 'ccd/login.html')


def logoutUser(request):
    logout(request)
    return redirect('ccd:login')

@login_required(login_url='ccd:login')
def studentDetails(request, rollNo):
    context = {}
    student = get_object_or_404(Student, rollNo=rollNo)
    context['student'] = student
    studentStates = State.objects.filter(student=student).order_by('-updatedOn').order_by('company')
    previousState = ""
    if studentStates.count() > 0:
        previousState = studentStates[0].company
    currentList = []
    allStates = []
    for state in studentStates:
        if state.company == previousState:
            currentList = [state] + currentList
        else:
            currentList = sorted(currentList, key=lambda x: x.updatedOn, reverse=True)
            allStates.append({ 'company': previousState, 'states': currentList})
            previousState = state.company
            currentList = []
            currentList = [state] + currentList
    currentList = sorted(currentList, key=lambda x: x.updatedOn, reverse=True)
    allStates.append({'company': previousState, 'states': currentList})

    context['allStates'] = allStates
    context['studentStates'] = studentStates
    company = Company.objects.all().order_by('name')
    context['company'] = company
    try:
        pref = RememberPreference.objects.get(user=request.user)
        context['pref'] = pref
    except Exception:
        pass
    return render(request, 'ccd/studentDetails.html', context)


def updateState(student, state, updateCurrentState):
    if state['description'] == '':
        return False
    company = Company.objects.get(name=state['company'])
    newState = State(student=student, description=state['description'], updatedBy=state['updatedBy'], company=company)
    newState.save()
    if updateCurrentState == True:
        student.lastState = newState.description
        student.lastUpdated = newState.updatedOn
        student.save()
    return True

@login_required(login_url='ccd:login')
def updateStateMain(request):
    if request.POST.get('companyPreference'):
        # try:
        obj, created = RememberPreference.objects.get_or_create(user=request.user,
                                                        defaults={'companyPreference': Company.objects.get(name=request.POST.get('companyName'))})
        if not created:
            obj.companyPreference = Company.objects.get(name=request.POST.get('companyName'))
            obj.save()
    student = get_object_or_404(Student, rollNo=request.POST['rollNo'])
    state = {
        'description' : request.POST['description'],
        'updatedBy': request.user,
        'company': request.POST.get('companyName'),
    }
    if updateState(student, state, True):
        messages.success(request, 'Successfully Updated!')
    else:
        messages.error(request, 'Invalid Request')
    return redirect('ccd:studentDetails', rollNo=student.rollNo)


@login_required(login_url='ccd:login')
def search(request):
    if request.method == "POST":
        context = {}
        if request.POST['search']:
            search = request.POST['search']
            searchedStudents = Student.objects.filter(Q(rollNo__icontains=search) | Q(name__icontains=search)).order_by('-lastUpdated')
            print(search, searchedStudents)
            context['allStudents'] = searchedStudents
        else:
            allStudents = Student.objects.all().order_by('-lastUpdated')
            context['allStudents'] = allStudents
        return render(request, 'ccd/index.html', context)
    else:
        return redirect('ccd:index')


@login_required(login_url='ccd:login')
def updateRequestState(request):
    student = get_object_or_404(Student, rollNo=request.POST['rollNo'])
    state = {
        'description': request.POST['description'],
        'updatedBy': request.user,
        'company': request.POST.get('companyName'),
    }
    if updateState(student, state, False):
        messages.success(request, 'Successfully Updated!')
    else:
        messages.error(request, 'Invalid Request')
    return redirect('ccd:studentDetails', rollNo=student.rollNo)


@login_required(login_url='ccd:login')
def updates(request):
    context = {}
    updates = Update.objects.all().order_by('-addedOn')
    context['updates'] = updates
    return render(request, 'ccd/updates.html', context)

@login_required(login_url='ccd:login')
def uploadData(request):
    if request.user.is_superuser:
        return render(request, 'ccd/uploadData.html')

@login_required(login_url='ccd:login')
def uploadModelFile(request):
    if request.user.is_superuser:
        studentCsv = request.FILES.get("studentCsv")
        if studentCsv:
            studentAdded = 0
            reader = csv.reader(codecs.iterdecode(studentCsv, 'utf-8'))
            print(reader)
            for row in reader:
                obj, created = Student.objects.update_or_create(
                    rollNo=row[1],
                    defaults={
                        'name': row[0],
                        'lastUpdated' : datetime.utcnow().replace(tzinfo=utc),
                        'comments' : row[2],
                    },

                )
                studentAdded = studentAdded + 1

            messages.success(request, str(studentAdded) + ' students added!')
        pocLogin  = request.FILES.get("pocLogin")
        if pocLogin:
            pocLoginAdded = 0
            reader = csv.reader(codecs.iterdecode(pocLogin, 'utf-8'))
            print(reader)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="credentials.csv"'

            writer = csv.writer(response)
            for row in reader:
                username = row[0]
                password = row[1]
                count = 1
                while True:
                    try:
                        testUsernameExists = User.objects.get(username=username)
                        username = str(username) + str(count)
                        count = count + 1
                    except Exception:
                        break

                user = User.objects.create_user(username, '', password)
                row[0] = username
                writer.writerow(row)
                pocLoginAdded = pocLoginAdded + 1
            return response
        companyCsv = request.FILES.get("companyCsv")
        if companyCsv:
            companyAdded = 0
            reader = csv.reader(codecs.iterdecode(companyCsv, 'utf-8'))
            print(reader)
            for row in reader:
                obj, created = Company.objects.update_or_create(
                    name=row[0],
                    defaults={
                        'description': row[0],
                    },

                )
                companyAdded = companyAdded + 1

            messages.success(request, str(companyAdded) + ' company added!')
        return render(request, 'ccd/uploadData.html')



@login_required(login_url='ccd:login')
def changepassword(request):
    if request.method == "POST":
        try:
            print(request.user)
            user1 = User.objects.get(username=request.user)
            user1.set_password(request.POST.get('password'))
            user1.save()
            messages.success(request, 'Password reset successfully. Login with your new Password')
            return render(request, 'ccd/changepassword.html')
        except Exception as e:
            print(e)
            messages.error(request, 'Error. Contact Admin')
            return render(request, 'ccd/changepassword.html')
    else:
        return render(request, 'ccd/changepassword.html')