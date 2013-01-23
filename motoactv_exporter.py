#!/usr/bin/python
' Checks for latest workout on Motoactv-portal and converts to TCX and uploads them to a web training site.'
' Motoactv Credentials:'

from stravaUpload import UploadToStrava
from motoactv import DownloadFromPortal
from motoactv_tcx import convertTCX
import os
import sys

def move(src,dst):
    os.system ("mv"+ " " + src + " " + dst)

def main():

    moto_email = ''
    moto_pass = ''

    strava_email = ''
    strava_pass = ''

    filenamecsv = DownloadFromPortal(moto_email, moto_pass)
    if(filenamecsv == 'null'):
        print 'Done'
        return

    print 'Downloaded: ' + filenamecsv

    print "Converting ..."

    # better converter
    tcxfile = convertTCX(filenamecsv)

    # use tidy to clean up non-indented xml file
    os.system("tidy -i -q -xml -f tidy_errs.txt -m " + tcxfile)

    print 'uploading ' + tcxfile + '...'

    # upload TCX to Strava
    UploadToStrava(tcxfile, strava_email, strava_pass)
    
    #move files for permanent storage
    print 'moving files ...'
    move(filenamecsv, './MotoBackups/'+filenamecsv)
    move(tcxfile, './TCXBackups/'+tcxfile)

main()
