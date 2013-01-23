#!/usr/bin/python

import urllib, urllib2, cookielib, re, os, sys
from datetime import date

class Motoactv():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cj),
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0))

        self.opener = opener

    def login(self):
        url = "https://www.motoactv.com/session/login.json"
        'construct the payload'
        data = "screen_name="+self.email+"&password="+self.password+"&remember_me=1"

        'get the cookies'
        usock = self.opener.open("https://www.motoactv.com/")
        'login to the site'
        usock = self.opener.open(url+"?"+data)
        if '{"code":"1","return_url":"/dashboard/index"}' in usock.read():
            print "MOTO - Logged in."
        else:
            print "MOTO - Failed login"
            print usock.read()
            sys.exit()
    
    def getLatestWorkout(self, ActivityId):
        'usock = self.opener.open("https://motoactv.com/settings/export")'
        usock = self.opener.open("https://motoactv.com/workout/show")
        lineList = usock.readlines()
        for line in lineList:
            if '<span>Download</span></a> (.csv)' in line:
                   pos = line.find('Id=')
                   line = line[pos+3:]
                   pos = line.find('">')
                   line = line[:pos]
                   ActivityId[0] = line
                   return
        print 'Latest workout not found'
        return

    def download(self, ActivityId, filename):
        file_name = ActivityId + '.csv'
        f = open(file_name, 'w')
        filename[0] = file_name
        u = self.opener.open("https://motoactv.com/workout/rawDataCsv.csv?workoutActivityId=" + ActivityId)
        meta = u.info()
        print meta
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
            
        f.close()
        return
        
def checkMotoActivities(ActivityId):
    try:
        f = open('MotoActivities', 'r') 
    except IOError as e:
        print 'No past workouts - ./MotoActivities not found'
        return 1
    lineList = f.readlines()
    f.close()
    #loop over the lines in the file and find first line that is not blank
    j = -1
    for i in reversed(xrange(len(lineList))):
        if(lineList[i] != '\n'):
            j = i
            break
    print 'Most recent activity: ' + str(lineList[j])
    #check activity id plus newline against line in file
    if(str(lineList[j]) != (str(ActivityId)+'\n')):
        print 'New activity: ' + str(ActivityId)
        return 1
    else:
        print 'No new activity'
        return 0

def writeMotoActivities(ActivityId):
    f = open('MotoActivities', 'a+')
    f.write('MotoActivities\n')
    f.write('----------------------------------------\n')
    td = date.today();
    td = td.strftime('%Y-%m-%d\n')
    f.write(td)
    f.write(ActivityId+'\n\n')
    return

def DownloadFromPortal(email, password):
    m = Motoactv(email, password)
    m.login()
    ActivityId = ['stupid immutable objects...']
    m.getLatestWorkout(ActivityId)
    if checkMotoActivities(ActivityId[0]):
        filename = ['stupid immutable objects...']
        m.download(ActivityId[0], filename)
        writeMotoActivities(ActivityId[0])
        return filename[0]
    else:
        return 'null'
