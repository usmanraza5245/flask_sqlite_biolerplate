from config.db import db

class User():

    def __init__(self, firstName,lastName,email,password,username):
        self.firstName =firstName
        self.lastName =lastName
        self.username =username
        self.email =email
        self.password =password


    def __str__(self):
        return f" >>>  User({self.username},{self.email},{self.firstName},{self.lastName},{self.password})"
         
    def __repr__(self):
        rep = 'User(' + self.username + ',' + str(self.email) + ')'
        return rep

    @staticmethod
    def UserExists(query):
        user=db.users.find_one(query)
        if user:
            return user
        else:
            return False
    
    def serialize(self):
            return {
                '_id': str(self._id),
                'firstName': self.firstName,
                'lastName': self.lastName,
                'username': self.username,
                'email': self.email,
                'password': self.password,
            }


    def toDictionary(self):
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }
        
            


    @staticmethod
    def from_dict(user_dict):
        return User(user_dict['username'], user_dict['password'], user_dict['email'])

    @staticmethod
    def seed():
        db.users.delete_many({})
        user1 = User(
        firstName='alice',
        lastName='stone',
        username='alice',
        password='pakistan123>',
        email='alice@gmail.com'
    )
        user2 = User(
        firstName='bob',
        lastName='stone',
        username='bob',
        password='pakistan123>',
        email='bob@gmail.com'
    )
        user3 = User(
        firstName='carson',
        lastName='stone',
        username='carson',
        password='pakistan123>',
        email='carson@gmail.com'
    )
        user1=db.users.insert_one(user1.toDictionary())
        user2=db.users.insert_one(user2.toDictionary())
        user3=db.users.insert_one(user3.toDictionary())
        users=db.users.find()
        data=[]
        for user in users:
            data.append({"_id": str(user["_id"]),"username":user["username"],"firstName":user["firstName"],"lastName":user["lastName"],"email":user["email"]})
        return data

        
