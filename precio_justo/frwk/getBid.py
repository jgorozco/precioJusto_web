from frwk.data import Constants, JSONUtils
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
             #   self.createData()
                listBids=list()
                queryMyBids='WHERE userBidder= :1'
                queryBidsRandom='WHERE userPropietary!= :1'
                bidsDone=BidResult.gql(queryMyBids,user).fetch(1000,0)
                b=Bid.gql('').fetch(1000, 0)
                logging.info('number of elements :'+str(len(b)))
                bidsParticipate=list()
                for b in bidsDone:
                    bidsParticipate.append(b.bidBidder)
                offset=0
                numBids=Constants.NUM_MAX_BIDLIST
                rand=random.random()
                logging.info('len:'+str(len(bidsParticipate)))
                repeats=0
                while len(listBids)<int(numBids):
                    rand=random.random()
                    bids=Bid.gql(queryBidsRandom,user).fetch(20,offset)
                    offset+=Constants.NUM_MAX_BIDLIST
                    #TODO
                    # while len(bids)>0
                    #b=bids.pop(random.random(0,len(bid))
                    #randm=random.uniform(0,len(bids))
                    for b in bids:
                        if b not in bidsParticipate:
                            if b not in listBids:
                                listBids.append(b)
                    if repeats>5:
                        break
                    else:
                        repeats=repeats+1
                returnData=JSONUtils.serializeAnyObjToJSON(listBids)
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
                returnData='{ "timelstamp": "'+str(time.time())+'"}'
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
        dataReturned=Constants.ERROR_BAD_UNEXPECTED
        rand=random.random()
        if not myUser :
            logging.info('no user')
            dataReturned=Constants.ERROR_NO_USER
        else :
            logging.info('with user')
            actualDate=time.time()
            bidsDone=BidResult.gql('WHERE userBidder= :1',myUser)
            #AND timeStamp > :2 AND rand1 > :3  ORDER BY rand LIMIT 30
            #TODO revisar la consulta y ver si hay otra manera de hacerlo
            bids=Bid.gql('WHERE userPropietary = :1 AND  rand1 > :2 ORDER BY rand1 LIMIT 30',myUser,rand)
            logging.info('user bids:'+str(bids.count(100)))
            listBids=list()
            numTotal=Constants.NUM_MAX_BIDLIST
            while numTotal>listBids.count :
                for bid in bids :
                    if bid not in bidsDone :
                        listBids.append(bid)
                        if listBids.count>= numTotal:
                            break
            dataReturned=JSONUtils.serializeAnyObjToJSON(listBids)            
        
        return dataReturned

    def getSomeBids(self,numBids,user):
        listBids=list()
        queryMyBids='WHERE userBidder= :1'
        queryBidsRandom='WHERE userPropietary = :1 AND  rand1 > :2 ORDER BY rand1'
        bidsDone=BidResult.gql(queryMyBids,user).fetch(100, 0)
        offset=0
        rand=random.random()
        while listBids.count()<int(numBids):
            #rand=random.random()
            bids=Bid.gql(queryBidsRandom,user,rand).fetch(Constants.NUM_MAX_BIDLIST,offset)
            offset+=Constants.NUM_MAX_BIDLIST
            lisDiff=set(bids).difference(bidsDone).difference(listBids)
            listBids.extend(lisDiff)
            
            

    def getOldBids(self,myUser):
        actualDate=time.time()
        dataReturned=Constants.ERROR_BAD_UNEXPECTED
        rand=random.random()
        if not myUser:
            logging.info('no user')
            dataReturned=Constants.ERROR_NO_USER
            bids=Bid.gql('WHERE userPropietary != :1 AND timeStamp< :2  AND rand1 > :3  ORDER BY rand LIMIT :4',myUser,actualDate,rand,Constants.NUM_MAX_BIDLIST)
            dataReturned=JSONUtils.serializeAnyObjToJSON(bids)
        else :
            logging.info('with user')
            bidsDone=BidResult.gql('WHERE userBidder= :1',myUser)
            bids=Bid.gql('WHERE userPropietary != :1 AND timeStamp< :2 AND rand1 > :3  ORDER BY rand LIMIT 30',myUser,actualDate,rand)
            listBids=list()
            numTotal=Constants.NUM_MAX_BIDLIST
            while numTotal>listBids.count() :
                for bid in bids :
                    if bid not in bidsDone :
                        listBids.append(bid)
                        if listBids.count()>= numTotal:
                            break
            dataReturned=JSONUtils.serializeAnyObjToJSON(listBids)
        return dataReturned
#        for elem in bid._entity:
#            localAttr= getattr(bid, elem)
#            if isinstance(localAttr,db.Model) :
#                logging.info('the att '+elem+' is DB:'+str(localAttr.user))
#            else :
#                logging.info('the att '+elem+' is '+str(localAttr))
#        logging.info('_____________________________________')
 


            #logging.info('---:'+str(elem)+'=='+str(getattr(bid, elem)))
#        logging.info('USER:XML:: \n'+user.to_xml())
#        logging.info('USER:JSON:: \n'+simplejson.dumps(user.__dict__))
#        logging.info('BID:XML:: \n'+bid.to_xml())
        
        
        
      
#        logging.info('user:xml:'+serializers.serialize("xml", user))
#        logging.info('user:json:'+serializers.serialize("json", user))
#        logging.info('bid:xml:'+serializers.serialize("xml", bid))
#        logging.info('bid:json:'+serializers.serialize("json", bid))
       
       
       
       
