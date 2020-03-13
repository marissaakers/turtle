from turtleapi import db
from turtleapi.models.turtlemodels import Depredation
from sqlalchemy.orm import load_only, defer
from sqlalchemy import update

def add_depredation(data):
    depredation = Depredation.new_from_dict(data)
    db.session.add(depredation)
    db.session.commit()
    return 'Successfully added depredation'

def update_depredation(data):
    db.session.query(Depredation).filter_by(depredation_id=data['depredation_id']).update(data)
    db.session.commit()
    return 'Successfully updated false crawl'

def get_depredations():
    query_result = db.session.query(Depredation).all()
    result_dict = [x.to_dict() for x in query_result]

    return result_dict

def delete_depredation(depredation_id):
    db.session.query(Depredation).filter_by(depredation_id=depredation_id).delete()
    db.session.commit()
    return 'Successfully deleted depredation'