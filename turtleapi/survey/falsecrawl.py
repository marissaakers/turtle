from turtleapi import db
from turtleapi.models.turtlemodels import FalseCrawl
from sqlalchemy.orm import load_only, defer
from sqlalchemy import update

def add_false_crawl(data):
    falsecrawl = FalseCrawl.new_from_dict(data)
    db.session.add(falsecrawl)
    db.session.commit()
    return 'Successfully added false crawl'

def update_false_crawl(data):
    # TODO: figure out why the JSON is coming over with booleans as strings.
    data['project_area'] = True if data['project_area'] == 'true' else False
    data['hit_scarp_over_18'] = True if data['hit_scarp_over_18'] == 'true' else False
    db.session.query(FalseCrawl).filter_by(false_crawl_id=data['false_crawl_id']).update(data)
    db.session.commit()
    return 'Successfully updated false crawl'

def get_false_crawls():
    query_result = db.session.query(FalseCrawl).all()
    result_dict = [x.to_dict() for x in query_result]

    return result_dict

def delete_false_crawl(false_crawl_id):
    db.session.query(FalseCrawl).filter_by(false_crawl_id=false_crawl_id).delete()
    db.session.commit()
    return 'Successfully deleted false crawl'