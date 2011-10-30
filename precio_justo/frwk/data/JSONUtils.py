from google.appengine.api.users import User
from google.appengine.ext import db
import simplejson
import logging

class JSONUtils(object):


    @staticmethod
    def get_class( kls ):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m

    @staticmethod
    def createOrUpdateDbElementsFromDICT(localDict):
        obj=None
        if localDict.has_key('id'):
            localId=str(localDict['id'])
            nameId=localId.split(':')[0]
            classObject=localId.split(':')[1]
            dbModel = JSONUtils.get_class( 'frwk.data.DataModel.'+classObject )
            obj=dbModel().get_by_id(long(nameId))
        else :
            return None
        if obj==None : #create obj
            obj=dbModel()      
        for attrName in localDict.keys() :
            attrValue=localDict.get(attrName)
            putValue=attrValue
            if   isinstance(attrValue, dict) :
                putValue=JSONUtils.createOrUpdateDbElementsFromDICT(attrValue)
            elif isinstance(attrValue, list) :
                putValue=list()
                for element in attrValue :
                    if isinstance(element, dict) :
                        insideObj=JSONUtils.createOrUpdateDbElementsFromDICT(element)
                        putValue.append(insideObj.key())
                    else :
                        putValue.append(element)
            if not attrName=='id' :
                try :
                    setattr(obj, attrName, putValue)
                except Exception,e :
                    logging.info('ErrorExcp::'+str(e))
                    setattr(obj, attrName, User(putValue))
                finally:   
                    obj.put()        
        return obj

    @staticmethod
    def dumpAnyJSONInDB(JsonData):
        return JSONUtils.createOrUpdateDbElementsFromDICT(simplejson.loads(JsonData))
        
        
    @staticmethod    
    def generateComplexDictFromDb(localObject):
        if isinstance(localObject,db.Model):
            returnedObj={}
            returnedObj['id']=str(localObject.key().id_or_name())+':'+str(localObject.key().kind())
            for elem in localObject._entity:
                localAttr= getattr(localObject, elem)
                returnedObj[elem]=JSONUtils.generateComplexDictFromDb(localAttr)
            return returnedObj
        elif isinstance(localObject,str) or isinstance(localObject,unicode):
            return str(localObject)
        elif isinstance(localObject,int) or isinstance(localObject,long):
            return int(localObject)
        elif isinstance(localObject,User):
            return str(localObject.email())
        elif isinstance(localObject,list) or isinstance(localObject,db.GqlQuery):
            returnedList=list()
            for elem in localObject :
                localObj=JSONUtils.generateComplexDictFromDb(elem)
                returnedList.append(localObj)
            return returnedList
        elif isinstance(localObject, db.Key) :
            modelObj=db.get(localObject)
            return JSONUtils.generateComplexDictFromDb(modelObj)
        else :
            return str(localObject)
        
    @staticmethod
    def serializeAnyObjToJSON(anyObject):
        return simplejson.dumps(JSONUtils.generateComplexDictFromDb(anyObject))
        