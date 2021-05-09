from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from noteApp.models import Note
from modules.log import * 
import json

# Create your views here.

def index(request):
    if request.user.is_authenticated:   
        if request.user.is_superuser:   
            return redirect('adminDashboard')  
        else:
            applicationLog('Error','<' + request.user.username + '> kullanıcısı yetkisiz DASHBOARD görüntüleme girişiminde bulundu.')
            return render(request, '401Page.html')   
    else:
        return render(request,'adminLogin.html')

def adminLogin(request):
    if request.user.is_authenticated:
        if request.user.is_staff:   
            return redirect('index')
        else:
            return render(request,'401Page.html')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user and user.is_superuser:
                login(request, user)                
                loginLog('Info','<' + username + '> Uygulamaya basariyla giris yapti' )
                return redirect('index')
            else:
                loginLog('Warning','<' + username + '> Hatalı giriş denemesi yapıldı.' )
                return index(request)
        else:
            return redirect('index')


def adminLogout(request):
    username = request.user.username
    logout(request)    
    loginLog('Info','<' + username + '> Uygulamadan güvenli çıkış yaptı.' )
    return redirect('/administration')

def admin_check(request):
    return user.is_staff

@login_required(login_url='/administration')
def adminDashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        notes = Note.objects.all()
        context = {
            'users' :   users,
            'notes' :   notes
        }
        
        applicationLog('Info','<' + request.user.username + '> kullanıcısı tarafından DASHBOARD görüntülendi.')

        return render(request, 'admin/dashboard.html', context)
    else:
        applicationLog('Warning','<' + request.user.username + '> kullanıcısı yetkisiz DASHBOARD görüntüleme girişiminde bulundu.')
        return render(request,'401Page.html')


@login_required(login_url='/administration')
def newUserPage(request):
    if request.user.is_superuser:
        return render(request,'admin/newUserPage.html')
    else:
        return render(request,'401page.html')


@login_required(login_url='/administration')
def createNewUser(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            userData = parseUserData(request)
            if userData['password'] == userData['repassword']:
                if not User.objects.filter(username = userData['username']).exists():
                    if not User.objects.filter(email=userData['email']).exists():
                        user = User.objects.create_user(username=userData['username'], password=userData['password'], email=userData['email'], is_staff=userData['is_staff'])
                        user.save()
                        applicationLog('Info','<' + request.user.username + '> kullanıcısı ' + userData['username'] + ' adlı kullanıcıyı sisteme ekledi.')
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
    else:
        applicationLog('Error','<' + request.user.username + '> kullanıcısı tarafından yetkisiz kullanıcı ekleme girişimi yapıldı.')
        return render(request,'401page.html')
        

@login_required(login_url='/administraition')
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


@login_required(login_url='/administraition')
def delete_note(request):
    if request.user.is_superuser:
        if request.method == "POST":
            noteID = request.POST['id']
            Note.objects.filter(id=noteID).delete()   
            applicationLog('Info','<' + request.user.username + '> kullanıcısı tarafından ' + str(noteID) + ' ID nolu not silindi.') 
            return HttpResponse(json.dumps({'message':'note silindi.'}))
    else:
        applicationLog('Error','<' + request.user.username + '> kullanıcısı yetkisiz not silme girişiminde bulundu.')
        return render(request,'401page.html')
 


@login_required(login_url='/administraition')
def delete_user(request):
    if request.user.is_superuser:
        if request.method == "POST":
            userName = request.POST['username']
            User.objects.filter(username=userName).delete()
            Note.objects.filter(username=userName).delete()
            applicationLog('Info','<' + request.user.username + '> kullanıcısı tarafından ' + userName + ' adlı kullanıcı silindi.' )
            return HttpResponse(json.dumps({'message':'User and notes deleted with succesfully.'}))
    else:
        applicationLog('Error','<' + request.user.username + '> kullanıcısı yetkisiz kullanıcı silme girişiminde bulundu.')
        return render(request,'401page.html')