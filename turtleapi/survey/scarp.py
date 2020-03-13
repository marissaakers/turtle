from turtleapi import db
from turtleapi.models.turtlemodels import Scarp
from sqlalchemy.orm import load_only, defer
from sqlalchemy import update

def add_scarp(data):
    scarp = Scarp.new_from_dict(data)
    db.session.add(scarp)
    db.session.commit()
    return 'Successfully added scarp'

def update_scarp(data):
    db.session.query(Scarp).filter_by(scarp_id=data['scarp_id']).update(data)
    db.session.commit()
    return 'Successfully updated scarp'

def get_scarps():
    query_result = db.session.query(Scarp).all()
    result_dict = [x.to_dict() for x in query_result]

    return result_dict

def delete_scarp(scarp_id):
    db.session.query(Scarp).filter_by(scarp_id=scarp_id).delete()
    db.session.commit()
    return 'Successfully deleted scarp'