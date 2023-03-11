from config.db import db

class Target():

    def __init__(self, targetType,targets,user):
        self.targetType =targetType
        self.targets =targets
        self.user =user


    def __str__(self):
        return f" >>>  Target({self.targetType},{self.targets},{self.user})"
         
    def __repr__(self):
        rep = 'Target(' + self.targetType + ',' + str(self.targets) + ')'
        return rep

    @staticmethod
    def TargetExist(query):
        target=db.targets.find_one(query)
        if target:
            return target
        else:
            return False
    
    def serialize(self):
            return {
                '_id': str(self._id),
                'targetType': self.targetType,
                'targets': self.targets,
                'user': self.user,
            }


    def toDictionary(self):
        return {
            'targetType': self.targetType,
            'targets': self.targets,
            'user': self.user,
        }
        
            


    

    @staticmethod
    def seed():
        db.targets.delete_many({})
        user1 = Target(
        targetType='alice',
        targets='stone',
        username='alice',
        password='pakistan123>',
        user='alice@gmail.com'
    )
        user2 = Target(
        targetType='bob',
        targets='stone',
        username='bob',
        password='pakistan123>',
        user='bob@gmail.com'
    )
        user3 = Target(
        targetType='carson',
        targets='stone',
        username='carson',
        password='pakistan123>',
        user='carson@gmail.com'
    )
        user1=db.targets.insert_one(user1.toDictionary())
        user2=db.targets.insert_one(user2.toDictionary())
        user3=db.targets.insert_one(user3.toDictionary())
        targets=db.targets.find()
        data=[]
        for user in targets:
            data.append({"_id": str(user["_id"]),"username":user["username"],"targetType":user["targetType"],"targets":user["targets"],"user":user["user"]})
        return data

        
