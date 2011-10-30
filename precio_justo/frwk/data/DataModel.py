from google.appengine.ext import db

 
class UserData(db.Model):
    myUser=db.UserProperty()
    nickUser= db.StringProperty()
    totalScore=db.FloatProperty()
    monthScore=db.FloatProperty()
    
    
class UserAchievements(db.Model):
    user=db.UserProperty()
    achievement=db.StringProperty()       

    
class Bid(db.Model):
    userPropietary=db.UserProperty()
    urlPhoto=db.StringProperty()
    timeStamp=db.FloatProperty()
    urlData=db.StringProperty()
    description=db.StringProperty()
    price=db.FloatProperty()
    rand1=db.FloatProperty()
    
class BidResult(db.Model):
    userBidder=db.UserProperty()
    bidBidder=db.ReferenceProperty(Bid)
    bidPrice=db.FloatProperty()
    points=db.FloatProperty()
