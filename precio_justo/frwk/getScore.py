from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import UserData, Bid, BidResult
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time

class getScore(webapp.RequestHandler):
    
    def get(self):
        user= users.get_current_user()
        returned=Constants.ERROR_NO_USER
        listArguments=self.request.arguments()
        if len(listArguments)>0:
            argumentData=listArguments.pop()
            if argumentData==Constants.ARG_MYSCORE :
                returned=self.getUserDataScore()
            elif argumentData==Constants.ARG_ARCHIEVEMENTS:
                returned=self.getArchievements()
            elif argumentData==Constants.ARG_TOTALRANKING:
                returned=self.getTotalRanking()
            elif argumentData==Constants.ARG_MONTHRANKIN:
                returned=self.getMonthRanking()
            elif argumentData==Constants.ARG_GLOBALTIME:
                returned=self.getGlobalTime()
            else :
                returned=Constants.ERROR_BAD_ARGUMENT
            
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(returned)
        
    def getGlobalTime(self):
        return '{ "timelstamp": "'+str(time.time())+'"}'
  
        
    def getUserDataScore(self):
        return ''
    
    def getArchievements(self):
        return ''
    
    def getTotalRanking(self):
        return ''
    
    def getMonthRanking(self):
        return ''
        