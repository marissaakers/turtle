from turtleapi import db
from turtleapi.models.turtlemodels import BigSurvey

def insert_pafb(data):
    pafb = BigSurvey.new_from_dict(data)
    db.session.add(pafb)
    db.session.commit()
    return {'message':'no errors'}

def insert_mid_reach(data):
    mid_reach = BigSurvey.new_from_dict(data)
    db.session.add(mid_reach)
    db.session.commit()
    return {'message':'no errors'}

def insert_south_reach(data):
    south_reach = BigSurvey.new_from_dict(data)
    db.session.add(south_reach)
    db.session.commit()
    return {'message':'no errors'}