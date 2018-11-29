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
        allStudents = Student.objects.all().order_by('-lastUpdated')
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
                return HttpResponseRedirect(request.POST['next'], 'store:index')
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
    studentStates = State.objects.filter(student=student).order_by('-updatedOn')
    context['studentStates'] = studentStates
    return render(request, 'ccd/studentDetails.html', context)

def updateState(student, state, updateCurrentState):
    if state['description'] == '':
        return False
    newState = State(student=student, description=state['description'], updatedBy=state['updatedBy'])
    newState.save()
    if updateCurrentState == True:
        student.lastState = newState.description
        student.lastUpdated = newState.updatedOn
        student.save()
    return True

@login_required(login_url='ccd:login')
def updateStateMain(request):
    student = get_object_or_404(Student, rollNo=request.POST['rollNo'])
    state = {
        'description' : request.POST['description'],
        'updatedBy': request.user,
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
            messages.success(request, str(pocLoginAdded) + ' login added!')
            return response
        return render(request, 'ccd/uploadData.html')
