from error import NotFoundError, ShadowManagementError, LogsError
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from models import ShadowManager, Logs
from app import db,api
from datetime import datetime

#API for ShadoWManager

ShadowManager_fields={
  "user_id" : fields.Integer, 
  "shadow_id" : fields.Integer, 
  "shadow_name" : fields.String, 
  "about" : fields.String, 
  "shadow_type" : fields.String, 
  "last_seen" : fields.String
}

create_shadow_parser=reqparse.RequestParser()
create_shadow_parser.add_argument('shadow_name')
create_shadow_parser.add_argument('about')
create_shadow_parser.add_argument('shadow_type')



update_shadow_parser=reqparse.RequestParser()
update_shadow_parser.add_argument('shadow_name')
update_shadow_parser.add_argument('about')
update_shadow_parser.add_argument('shadow_type')




class ShadowManagerAPI(Resource):
  @marshal_with(ShadowManager_fields)
  def get(self, user_id, shadow_id):
    shadow = ShadowManager.query.filter_by(user_id=user_id, shadow_id=shadow_id).first()
    if shadow:
      return shadow 
    else:
      raise  NotFoundError(status_code=404)
    
  @marshal_with(ShadowManager_fields)
  def put(self, user_id, shadow_id):
    args=update_shadow_parser.parse_args()
    shadow_name=args.get("shadow_name", None)
    about=args.get("about", None)
    shadow_type=args.get("shadow_type", None)

    if shadow_name is None:
      raise ShadowManagementError(status_code=400, error_code="SM1001", error_message="shadow_name is required")
    if about is None:
      raise ShadowManagementError(status_code=400, error_code="SM1002", error_message="about is required")
    if shadow_type is None:
      raise ShadowManagementError(status_code=400, error_code="SM1003", error_message="shadow_type is required")
    
    
    shadow = ShadowManager.query.filter_by(user_id=user_id, shadow_id=shadow_id).first()
    if shadow:
      shadow.shadow_name=shadow_name
      shadow.about=about
      shadow.shadow_type=shadow_type
      db.session.add(shadow)
      db.session.commit()
      return shadow
    else:
      raise NotFoundError(status_code=404)

    

  def delete(self, user_id, shadow_id):
    shadow = ShadowManager.query.filter_by(user_id=user_id, shadow_id=shadow_id).first()
    if shadow:
      db.session.delete(shadow)
      db.session.commit()  
      return "", 200
    else:
      raise  NotFoundError(status_code=404)
    
  
  
  def post(self, user_id):
    args=create_shadow_parser.parse_args()
    shadow_name=args.get("shadow_name", None)
    about=args.get("about", None)
    shadow_type=args.get("shadow_type", None)
    
    if shadow_name is None:
      raise ShadowManagementError(status_code=400, error_code="SM1001", error_message="shadow_name is required")
    if about is None:
      raise ShadowManagementError(status_code=400, error_code="SM1002", error_message="about is required")
    if shadow_type is None:
      raise ShadowManagementError(status_code=400, error_code="SM1003", error_message="shadow_type is required")

    new_record=ShadowManager(user_id=user_id, shadow_name=shadow_name, about=about, shadow_type=shadow_type, last_seen=datetime.now())
    db.session.add(new_record)
    db.session.commit()
    return "", 201

  


api.add_resource(ShadowManagerAPI, "/api/ShadowManager/<user_id>", "/api/ShadowManager/<user_id>/<shadow_id>")


#API for Logs

Log_fields={
  "user_id" : fields.Integer, 
  "shadow_id" : fields.Integer, 
  "log_id" : fields.Integer, 
  "time" : fields.String, 
  "value" : fields.String, 
  "note" : fields.String
}


update_log_parser=reqparse.RequestParser()
update_log_parser.add_argument('value')
update_log_parser.add_argument('note')


create_log_parser=reqparse.RequestParser()
create_log_parser.add_argument('value')
create_log_parser.add_argument('note')





class LogsAPI(Resource):
  @marshal_with(Log_fields)
  def get(self, user_id, shadow_id, log_id):
    log = Logs.query.filter_by(user_id=user_id, shadow_id=shadow_id, log_id=log_id).first()
    if log:
      return log
    else:
      raise  NotFoundError(status_code=404)

  
  @marshal_with(Log_fields)
  def put(self, user_id, shadow_id, log_id):
    args=update_log_parser.parse_args()
    value=args.get("value", None)
    note=args.get("note", None)
    

    if value is None:
      raise LogsError(status_code=400, error_code="LG1001", error_message="value is required")
    if note is None:
      raise LogsError(status_code=400, error_code="LG1002", error_message="note is required")
   
    
    
    log = Logs.query.filter_by(user_id=user_id, shadow_id=shadow_id, log_id=log_id).first()
    if log:
      log.value=value
      log.note=note 
      
      db.session.add(log)
      db.session.commit()
      return log
    else:
      raise NotFoundError(status_code=404)

  
  def delete(self, user_id, shadow_id, log_id):
    log = Logs.query.filter_by(user_id=user_id, shadow_id=shadow_id, log_id=log_id).first()
    if log:
      db.session.delete(log)
      db.session.commit()  
      return "", 200
    else:
      raise  NotFoundError(status_code=404)


  def post(self, user_id, shadow_id):
    args=create_log_parser.parse_args()
    value=args.get("value", None)
    note=args.get("note", None)
    
    
    if value is None:
      raise LogsError(status_code=400, error_code="LG1001", error_message="value is required")
    if note is None:
      raise LogsError(status_code=400, error_code="LG1002", error_message="note is required")
    

    new_record=Logs(user_id=user_id, shadow_id=shadow_id, time=datetime.now(), value=value, note=note)
    db.session.add(new_record)
    db.session.commit()
    return "", 201


api.add_resource(LogsAPI, "/api/Logs/<user_id>/<shadow_id>", "/api/Logs/<user_id>/<shadow_id>/<log_id>")