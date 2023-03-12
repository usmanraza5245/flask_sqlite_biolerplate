from config.db import db


class Target():

    def __init__(self, targetType, targets, user, limit, tweets=[], status=0):
        self.targetType = targetType
        self.targets = targets
        self.user = user
        self.limit = limit or 10
        self.tweets = tweets or []
        self.status = status or 0

    def __str__(self):
        return f" >>>  Target({self.targetType},{self.targets},{self.user})"

    def __repr__(self):
        rep = 'Target(' + self.targetType + ',' + str(self.targets) + ')'
        return rep

    @staticmethod
    def TargetExist(query):
        target = db.targets.find_one({'targetType': query['targetType']})
        if target:
            target["_id"] = str(target['_id'])
            target["user"] = str(target['user'])
            return target
        else:
            return False

    @staticmethod
    def GetUserTargets(authUser):
        data = []
        targets = db.targets.find({'user': authUser['_id']})
        for target in targets:
            target['_id'] = str(target['_id'])
            target['user'] = str(target['user'])
            data.append(target)
        return data

    def serialize(self):
        return {
            '_id': str(self._id),
            'targetType': self.targetType,
            'targets': self.targets,
            'user': self.user,
            'limit': self.limit,
            'tweets': self.tweets,
            'status': self.status,




        }

    def toDictionary(self):
        return {
            'targetType': self.targetType,
            'targets': self.targets,
            'user': self.user,
            'limit': self.limit,
            'tweets': self.tweets,
            'status': self.status,




        }
