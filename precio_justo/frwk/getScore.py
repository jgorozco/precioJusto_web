from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import UserData, Bid, BidResult
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time

class getScore(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(Constants.ERROR_BAD_REQUEST)