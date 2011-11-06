from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import Bid
from google.appengine.api import users
from google.appengine.ext import webapp
import time
from google.appengine.ext.key_range import simplejson

class uploadBid(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(Constants.ERROR_BAD_REQUEST)
    
    
    def post(self):
        user = users.get_current_user()
        returnedData=Constants.ERROR_NO_USER
        if user:
            dataRecived=self.request.body;
            bidRecived=simplejson.loads(dataRecived)
            if not bidRecived['userPropietary']==str(user.email()):
                returnedData=Constants.ERROR_BAD_USER
            else :
                bidRecived['timeStamp']=time.time()+bidRecived['timeStamp']
                returned=Bid(JSONUtils.JSONUtils.createOrUpdateDbElementsFromDICT(bidRecived,True))
                #TODO soporte a archievements
                if returned :
                    returnedData=Constants.RESULT_OK
                else :
                    returnedData=Constants.ERROR_BAD_DATA_POST
                    
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(returnedData)
            
            