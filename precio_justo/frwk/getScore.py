from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import UserData, Bid, BidResult, UserAchievements
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time

class getScore(webapp.RequestHandler):
    
    def get(self):
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
        user = users.get_current_user()
        returned=Constants.ERROR_NO_USER
        if user :
            myUserData=UserData.gql("WHERE myUser = :1",user)  
            userData=None
            if myUserData.count()>0:
                userData=myUserData.get()
                returned=JSONUtils.JSONUtils.serializeAnyObjToJSON(userData)
            else :
                returned=Constants.ERROR_BAD_USER
        return returned
    
    def getArchievements(self):
        user = users.get_current_user()
        returned=Constants.ERROR_NO_USER
        if user :
            archievements=UserAchievements.gql("WHERE user = :1",user)  
            returned=JSONUtils.JSONUtils.serializeAnyObjToJSON(archievements)
        return returned
    
    def getTotalRanking(self):
        users=UserData.gql("WHERE totalScore>0.0 ORDER BY totalScore DESC LIMIT 50 ").fetch(50, 0)
        return JSONUtils.JSONUtils.serializeAnyObjToJSON(users)
    
    def getMonthRanking(self):
        users=UserData.gql("WHERE monthScore>0.0 ORDER BY monthScore DESC LIMIT 50 ").fetch(50, 0)
        return JSONUtils.JSONUtils.serializeAnyObjToJSON(users)
        