from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from noteApp.models import Note
import json
# Create your views here.



def index(request):
    if request.user.is_authenticated:   
        if request.user.is_staff:   #superusersa erişsin
            return redirect('adminDashboard')  #---
        else:
            return render(request, '401Page.html')   #---
    else:
        return render(request,'adminLogin.html')

def adminLogin(request):    #---superuser değilse indexe gidemesin
    if request.user.is_authenticated:
        if request.user.is_staff:   #aslında gerek yok yukarıda kontrol ediyor
            return redirect('index')
        else:
            return render(request,'401Page.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_staff:
                login(request, user)
                print("Loged In Successfuly!")
                return redirect('index')
            else:
                print("Invalid username or password")
                return index(request)
        else:
            return redirect('index')


def adminLogout(request):
    logout(request)
    print("logouta geldi")
    return redirect('/administration')

def admin_check(request):
    return user.is_staff

@login_required(login_url='/administration')
def adminDashboard(request):
    users = User.objects.all()
    notes = Note.objects.all()
    context = {
        'users' :   users,
        'notes' :   notes
    }
    # toplam user sayısı
    # toplam not sayısı
    # son 10 not
    # 
    return render(request, 'admin/dashboard.html', context)

@login_required(login_url='/')
def newUserPage(request):
    return render(request,'admin/newUserPage.html')


@login_required(login_url='/')
def createNewUser(request):
    if request.method == 'POST':
        userData = parseUserData(request)
        if userData['password'] == userData['repassword']:
            if not User.objects.filter(username = userData['username']).exists():
                if not User.objects.filter(email=userData['email']).exists():
                    user = User.objects.create_user(username=userData['username'], password=userData['password'], email=userData['email'], is_staff=userData['is_staff'])
                    user.save()
                    print('user eklendi')
                    return redirect('index')
                else:
                    print('email zaten alinmis')
                    return redirect('newUserPage')
            else:
                print('kullanici zaten var.')
                return redirect('newUserPage')          
        else:
            print("parolalar eslesmiyor")
            return redirect('newUserPage')
        


def parseUserData(request):
    userData = {
        'username'  :   request.POST['username'],
        'email'     :   request.POST['email'],
        'password'  :   request.POST['password'],
        'repassword':   request.POST['repassword'],
        'is_staff'  :   ('is_staff' in request.POST),
        'is_admin'  :   ('is_admin' in request.POST),
        'is_visitor':   ('is_visitor' in request.POST)
    }

    return userData



def delete_note(request):    
    if request.method == "POST":
        noteID = request.POST['id']
        Note.objects.filter(id=noteID).delete()    
        return HttpResponse(json.dumps({'message':'note silindi.'}))


def delete_user(request):
    if request.method == "POST":
        userName = request.POST['username']
        User.objects.filter(username=userName).delete()
        Note.objects.filter(username=userName).delete()

        return HttpResponse(json.dumps({'message':'User and notes deleted with succesfully.'}))
