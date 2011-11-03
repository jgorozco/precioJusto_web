from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import UserData,  BidResult
from google.appengine._internal.django.utils.datetime_safe import datetime
from google.appengine.api import users
from google.appengine.ext import webapp

class setBidPrize(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(Constants.ERROR_BAD_REQUEST)
        
        
        
    def post(self):
        user = users.get_current_user()
        returned=Constants.ERROR_NO_USER
        if user :
            myBidResult=BidResult(JSONUtils.JSONUtils.dumpAnyJSONInDB(self.request.body))
            myUserData=UserData.gql('WHERE myUser =:1',user).get()
            if myUserData.myUser==user and myBidResult.userBidder==user:
                myUserData.totalScore+=int(myBidResult.points)
                now =datetime.datetime.now()
                if str(now.month)==myUserData.actualMonth:
                    myUserData.monthScore+=int(myBidResult.points)
                else:
                    myUserData.monthScore=int(myBidResult.points)
                    myUserData.actualMonth=str(now.month)
                myBidResult.put()
                #TODO soporte a archievements
            else:
                returned=Constants.ERROR_BAD_USER    
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(returned)