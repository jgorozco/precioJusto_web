from frwk.data import Constants, JSONUtils
from frwk.data.DataModel import UserData, Bid, BidResult
from google.appengine.api import users
from google.appengine.ext import webapp
import logging
import random
import time

class getBid(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        #chequear los argumentos
        listArguments=self.request.arguments()
        returnData=Constants.ERROR_NO_ARGUMENT
        if len(listArguments)>0:
            argumentData=listArguments.pop()
            if argumentData=='testall' :
                allbid=Bid.gql("WHERE userPropietary= :1",user)
                logging.info('number of bids_:'+str(Bid.all().count()))
                returnData=JSONUtils.JSONUtils.serializeAnyObjToJSON(allbid)
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
            dataReturned=JSONUtils.JSONUtils.serializeAnyObjToJSON(listBids)            
        
        return dataReturned

    def getOldBids(self,myUser):
        actualDate=time.time()
        dataReturned=Constants.ERROR_BAD_UNEXPECTED
        rand=random.random()
        if not myUser:
            logging.info('no user')
            dataReturned=Constants.ERROR_NO_USER
            bids=Bid.gql('WHERE userPropietary != :1 AND timeStamp< :2  AND rand1 > :3  ORDER BY rand LIMIT :4',myUser,actualDate,rand,Constants.NUM_MAX_BIDLIST)
            dataReturned=JSONUtils.JSONUtils.serializeAnyObjToJSON(bids)
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
            dataReturned=JSONUtils.JSONUtils.serializeAnyObjToJSON(listBids)
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
       
       
       
       
