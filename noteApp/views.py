from django.shortcuts import render
from django.http import *
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings

import json, os
import datetime
import sqlite3

from .models import Note


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return render(request,'login.html')


def login(request):    
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return redirect('/')
            else:
                print('Access Denied!')
                return index(request)

        


def logout(request):
    auth.logout(request)
    return render(request,"login.html")

@login_required(login_url="/")
def list_notes(request):    #-----------------------------------herkese kendi notu dönsün public hariç.
    noteList = Note.objects.all()
    noteObj = []

    for note in noteList:
        note = {
            'id'         :   note.id,
            'title'      :   str(note.title),
            'description':  str(note.description),
            'username'  :   str(note.username),
            'create_date':  str(note.create_date),
            'is_public' :   note.is_public   
        }
        noteObj.append(note)

    return HttpResponse(json.dumps(noteObj))

@login_required(login_url='/')
def detail_note(request):
    if request.user.is_staff:
        if request.method == 'POST':
            note_id = request.POST['noteID']
            note = Note.objects.filter(id=note_id)
            context = {
                'notes'  :   note
            }
            
            return render(request,'noteDetail.html',context)
    else:
        return render(request,'401Page.html')
       
    
@login_required(login_url='/')
def add_note(request):
    if request.user.is_staff:
        if request.method == 'POST':
            title = htmlEscape(request.POST['title'], 'encode')
            description = htmlEscape(request.POST['description'], 'encode')
            is_public = htmlEscape(request.POST['is_public'].capitalize(), 'encode')
            username = htmlEscape(request.user.username, 'encode')
            create_date = datetime.datetime.now()
            
            Note(
                title=title, 
                description=description, 
                username=username, 
                create_date=create_date, 
                is_public=is_public
            ).save()

        newNote = {
            'title'         :   title,
            'description'   :   description
        }
        
        return HttpResponse(json.dumps({'message':'Başarıyla Eklendi.'}))
    
    else:
        return render(request, '401Page.html')


    
@login_required(login_url='/')
def update_note(request):
    if request.user.is_staff:
        if request.method == 'POST':
            noteID = request.POST['noteID']
            title = htmlEscape(request.POST['title'], 'encode')
            description = htmlEscape(request.POST['description'], 'encode')
            is_public = ('is_public' in request.POST)

            Note.objects.filter(id=noteID).update(
                title = title,
                description = description,
                is_public = is_public
            )

            return redirect('/')

    else:
        return render(request,'401Page.html')

@login_required(login_url='/')
def delete_note(request):  
    if request.user.is_staff:  
        if request.method == "POST":
            noteID = request.POST['id']
            Note.objects.filter(id=noteID).delete()    
            return HttpResponse(json.dumps({'message':'note silindi.'}))
    
    else:
        return render(request,'401Page.html')


@login_required(login_url='/')
def search_page(request):
    if request.user.is_staff:
        return render(request, 'search.html')

    else:
        return render(request,'401Page.html')

@login_required(login_url='/')
def search_note(request):  
    if request.user.is_staff:
        if request.method == "POST":
            BASE_DIR = getattr(settings,"BASE_DIR", None)
            db_path = BASE_DIR + '/db.sqlite3'

            dbConnect = sqlite3.connect(db_path)
            dbCursor = dbConnect.cursor()
            keyword = cleanSpecialChar(request.POST['keyword'])

            
            sqlQuery = "SELECT * FROM noteApp_note WHERE  title LIKE '%"+keyword+"%'"
            print(sqlQuery)
            notes = dbCursor.execute(sqlQuery)

            print("-"*50)
            noteObj = []
            for note in notes:
                note = {
                    'id'        :   note[0],
                    'title'     :   str(note[1]),
                    'description':  str(note[2]),
                    'username'  :   str(note[3]),
                    'create_date':  str(note[4]),
                    'is_public' :   note[5]
                }
                noteObj.append(note)
            print("-"*20)
            print(noteObj)
            print("-"*20)
            dbConnect.close()

            return HttpResponse(json.dumps(noteObj))
    
    else:
        return render(request,'401Page.html')



def cleanSpecialChar(string):
    keyword = ''
    for char in string:
        if char.isalnum():
            keyword+=char
    
    return keyword

def htmlEscape(string, proc):
    codes = {
    '<' :   '&lt',
    '>' :   '&gt',
    '"' :   '&quot',
    "'" :   '&#x27'
    }

    if proc == 'encode':
        for key in codes.keys():
            string = string.replace(key, codes[key])
    
    if proc == 'decode':
        for key in codes.keys():
            string = string.replace(codes[key], key)

    return string




    