#!/usr/bin/python

import urllib, urllib2, cookielib, sys, json

class Strava():
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
        self.athlete_token = ''
        self.id = ''
        self.token = ''
        self.name = ''
        
    def get_web_data(self, url, values):
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        return json.loads(response.read())


    def parseAthleteToken(self):
        temp = self.athlete_token['athlete']
        self.id = temp['id'] 
        self.token = self.athlete_token['token']
        self.name = temp['name']

    def login(self):
        url = "https://www.strava.com/api/v2/authentication/login"
        data = {'email': self.email, 'password': self.password}
        jresp = self.get_web_data(url, data)
        self.athlete_token = jresp
        if self.athlete_token["token"]:
            print "STRAVA - Logged in."
            self.parseAthleteToken()
            athlete = jresp["athlete"]
            print "Welcome back " + self.name
        else:
            print "STRAVA - Failed login"
            print resp
            sys.exit()
  
    def upload(self, filename):
        f = open(filename)
        tcx = f.read()
        url = "http://www.strava.com/api/v2/upload"
        params = {'token': self.token,
                  'type': 'tcx',
                  'data': tcx
                  }
        jresp = self.get_web_data(url, params)
        upload_id = jresp['upload_id']
        return upload_id
        
    def mileage(self):
        "THIS API DOES NOT APPEAR TO BE FUNCTIONAL - TBD"
        url = "http://www.strava.com/api/v2/athletes"
        url += str(self.id)
        data = {'token': self.token}
        jresp = self.get_web_data(url, data)
        print jresp
        

def UploadToStrava(filename, email, passwd):            
    s = Strava(email, passwd)
    s.login()
    uploadid = s.upload(filename)
    print "Upload id: " + str(uploadid)

def main():
    if len(sys.argv) != 2:
           print( "Usage: " + sys.argv[0] + " <TCX file>")
           sys.exit(1) 
        
    pathToTCX = sys.argv[1]
    UploadToStrava(pathToTCX)
