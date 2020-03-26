from turtleapi import db
from turtleapi.models.turtlemodels import BigSurvey, Emergence

def insert_pafb(data):
    pafb = BigSurvey.new_from_dict(data)
    db.session.add(pafb)
    db.session.commit()
    return {'message':'no errors'}

def insert_mid_reach(data):
    mid_reach = BigSurvey()
    emergences = []

    for item in data.items():
        if item[0] == 'emergences':
            for em in item[1]:
                emergences.append(Emergence(**em))
        else:
            setattr(mid_reach, item[0], item[1])

    mid_reach.emergences = emergences
    db.session.add(mid_reach)
    db.session.commit()
    return {'message':'no errors'}

def insert_south_reach(data):
    south_reach = BigSurvey.new_from_dict(data)
    db.session.add(south_reach)
    db.session.commit()
    return {'message':'no errors'}