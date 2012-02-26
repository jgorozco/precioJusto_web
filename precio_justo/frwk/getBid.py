from frwk.data import Constants
from frwk.data.DataModel import Bid, BidResult
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time
from frwk.data.JSONUtils import JSONUtils

class getBid(webapp.RequestHandler):
    
    
        
           
        
    
    def get(self):
        logging.info('_______get all bids________')
        user = users.get_current_user()
        listArguments=self.request.arguments()
        returnData=Constants.ERROR_NO_ARGUMENT
        #self.createData()
        if len(listArguments)>0:
            argumentData=listArguments.pop()
            if argumentData=='testall' :
            #    self.createData()
                if user:
                    returnData=str(user.nickname())+':'+str(user.email())
                else:
                    returnData=self.getRandomBids()   
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
                returnData=self.getRandomBids()   
        else :
            returnData=self.getRandomBids()  
        self.response.headers['Content-Type'] = 'text/plain'
        logging.info('out::'+returnData)
        self.response.out.write(returnData)

    def createData(self):
            #creamos 3 bids mias
            bid1=Bid()
            bid1.description='description bid 1'
            bid1.price=5.0
            bid1.timeStamp=float(123)
            bid1.rand1=random.random()
            #bid1.userPropietary=users.get_current_user()
            bid1.put()



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
        
    def getRandomBids(self):
        listBids=list()
        repeats=0
        while len(listBids)<int(Constants.NUM_MAX_BIDLIST):
            bids=Bid.all().fetch(30, 0)
            while (len(bids)>0) and (len(listBids)<Constants.NUM_MAX_BIDLIST):
                ran=int(random.uniform(0,len(bids)-1))
                #logging.info('elemento:'+ran)
                b=bids.pop(ran)
                logging.info('datos:'+b.description)
                if b not in listBids:
                    listBids.append(b)
                    repeats=0
            if repeats>5:
                break
            else:
                repeats=repeats+1
                    
        return JSONUtils.serializeAnyObjToJSON(listBids)        
    
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
            bids=Bid.gql(queryBidsRandom,myUser.email()).fetch(20,offset)
            offset+=Constants.NUM_MAX_BIDLIST
            while len(bids)>0:
                #logging.info('tenemos :'+str(int(len(bids))))
                ran=int(random.uniform(0,len(bids)-1))
                #logging.info('cogemos el:'+str(int(ran)))
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
                            listBids.append(b)
            if repeats>5:
                break
            else:
                repeats=repeats+1
        return JSONUtils.serializeAnyObjToJSON(listBids)

       
