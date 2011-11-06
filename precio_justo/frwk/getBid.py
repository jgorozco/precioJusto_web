from frwk.data import Constants
from frwk.data.DataModel import UserData, Bid, BidResult
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time
from frwk.data.JSONUtils import JSONUtils

class getBid(webapp.RequestHandler):
    
    
        
           
        
    
    def get(self):
       
        user = users.get_current_user()
        listArguments=self.request.arguments()
        returnData=Constants.ERROR_NO_ARGUMENT
        if len(listArguments)>0:
            argumentData=listArguments.pop()
            if argumentData=='testall' :
            #    self.createData()
                if user:
                    returnData=str(user.nickname())+':'+str(user.email())
                else:
                    returnData=Constants.ERROR_NO_USER
#                allbid=Bid.gql("WHERE userPropietary= :1",user)
#                logging.info('number of bids_:'+str(Bid.all().count()))
#                returnData=JSONUtils.JSONUtils.serializeAnyObjToJSON(allbid)
            elif argumentData==Constants.ARG_OLDBIDS :
                logging.info('get a random old bids')
                returnData=self.getOldBids(user)
            elif argumentData==Constants.ARG_NEWRANDOM:
                logging.info('get a random new bids')
                returnData=self.getNewBids(user)
            elif argumentData==Constants.ARG_GLOBALTIME:
                logging.info('get global time')
                returnData='{ "timestamp": "'+str(time.time())+'"}'
            else :
                returnData=Constants.ERROR_BAD_ARGUMENT      
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(returnData)

    def createData(self):
            #creamos 3 bids mias
            bid1=Bid()
            bid1.description='description bid 1'
            bid1.price=5.0
            bid1.timeStamp=float(123)
            bid1.rand1=random.random()
            bid1.userPropietary=users.get_current_user()
            bid1.put()
    
            bid2=Bid()
            bid2.description='description bid 2'
            bid2.price=float(5)
            bid2.rand1=random.random()
            bid2.timeStamp=float(123)
            bid2.userPropietary=users.get_current_user()
            bid2.put()
            
            bid3=Bid()
            bid3.description='description bid 3'
            bid3.price=float(5)
            bid3.rand1=random.random()
            bid3.timeStamp=float(123)
            bid3.userPropietary=users.get_current_user()
            bid3.put()        
        
            #creo otras 3 que no son mias
            bid4=Bid()
            bid4.description='description bid 4'
            bid4.price=float(5)
            bid4.rand1=random.random()
            bid4.timeStamp=float(123)
            bid4.userPropietary=None
            bid4.put()
    
            bid5=Bid()
            bid5.description='description bid 5'
            bid5.price=float(5)
            bid5.rand1=random.random()
            bid5.timeStamp=float(123)
            bid5.userPropietary=None
            bid5.put()
            
            bid6=Bid()
            bid6.description='description bid 6'
            bid6.price=float(5)
            bid6.rand1=random.random()
            bid6.timeStamp=float(123)
            bid6.userPropietary=None
            bid6.put()    
            
            #el usuario ya ha hecho un bid en una de ellas
            bidResult=BidResult()
            bidResult.bidBidder=bid6
            bidResult.userBidder=users.get_current_user()
            bidResult.bidPrice=float(3)
            BidResult.points=float(30)
            bidResult.put()


    def getNewBids(self,myUser):
        if myUser:
            return self.getBids(myUser,'more')  
        else:
            return Constants.ERROR_NO_USER
        
    def getSomeBids(self,myUser):
        return self.getBids(myUser)
            
            

    def getOldBids(self,myUser):
        if myUser:
            return self.getBids(myUser,'less')
        else:
            return Constants.ERROR_NO_USER
    def getBids(self,myUser,localTime):
        listBids=list()
        queryMyBids='WHERE userBidder= :1'
        queryBidsRandom='WHERE userPropietary!= :1'
        bidsDone=BidResult.gql(queryMyBids,myUser).fetch(1000,0)
        b=Bid.gql('').fetch(1000, 0)
        # logging.info('number of elements :'+str(len(b)))
        bidsParticipate=list()
        for b in bidsDone:
            bidsParticipate.append(b.bidBidder)
        offset=0
        numBids=Constants.NUM_MAX_BIDLIST
        # logging.info('len:'+str(len(bidsParticipate)))
        repeats=0
        while len(listBids)<int(numBids):
            bids=Bid.gql(queryBidsRandom,myUser).fetch(20,offset)
            offset+=Constants.NUM_MAX_BIDLIST
            while len(bids)>0:
                logging.info('tenemos :'+str(int(len(bids))))
                ran=int(random.uniform(0,len(bids)))
                logging.info('cogemos el:'+str(int(ran)))
                b=bids.pop(ran)
                if localTime:
                    if localTime=='less':
                        if b.timeStamp>time.time():
                            b=None
                    else:
                        if b.timeStamp<time.time():
                            b=None
                else:
                    b=None  
                if b and b not in bidsParticipate:
                    if b not in listBids:
                        logging.info('ponemos:'+str(b.userPropietary))
                        listBids.append(b)
            if repeats>5:
                break
            else:
                repeats=repeats+1
        return JSONUtils.serializeAnyObjToJSON(listBids)

       
