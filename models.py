from app import db



class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True, nullable = False)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    
  
class ShadowManager(db.Model):
    __tablename__ = 'ShadowManager'
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    shadow_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key=True)
    shadow_name = db.Column(db.String)
    about = db.Column(db.String)
    shadow_type = db.Column(db.String)
    last_seen = db.Column(db.String)
    

class Logs(db.Model):
    __tablename__ = "Logs"
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    shadow_id = db.Column(db.Integer, db.ForeignKey("ShadowManager.shadow_id"))
    log_id = db.Column(db.Integer, autoincrement = True, unique=True, primary_key=True)
    time = db.Column(db.DateTime, nullable = False)
    value = db.Column(db.String, nullable = False)
    note = db.Column(db.String, nullable = False)