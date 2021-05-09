#!/usr/bin/python
#-*- coding:utf-8 -*-
#Author: @hsnbskn

from django.conf import settings
import datetime
import os

LOG_PATH = getattr(settings, "BASE_DIR", None)+"/quicknoteLOG"
LOGIN_LOGFILE = LOG_PATH + "/login.log"
QUICKNOTE_LOGFILE = LOG_PATH + "/application.log"
RUNTIME_ERR_LOGFILE = LOG_PATH + "/runtimeErr.log"


def directory_check():
    if not os.path.exists(LOG_PATH):
        try:
            os.mkdir(LOG_PATH)
        except:
            print("Log dizini olusturuladi")
            return False
    
    return True


def loginLog(level, msg):
    if directory_check():
        logFile = open(LOGIN_LOGFILE, 'a')
        time = str(datetime.datetime.now())
        logFile.write(level + " -> " + time + " -> " + msg + "\n")
        logFile.close()


def applicationLog(level, msg):
    if directory_check():
        logFile = open(QUICKNOTE_LOGFILE, 'a')
        time = str(datetime.datetime.now())   
        logFile.write(level + " -> " + time + " -> " + msg + "\n")
        logFile.close()


def runtimeErrorLog(level, msg):
    if directory_check():
        logFile = open(RUNTIME_ERR_LOGFILE, 'a')
        time = str(datetime.datetime.now()) 		
        logFile.write(level + " -> " + time + " -> " + msg + "\n")
        logFile.close()
