from turtleapi import db
from turtleapi.models.turtlemodels import FilterSet
from sqlalchemy import or_
import json
from flask import Response

def list_survey_filters(username):
    results = db.session.query(FilterSet.filter_set_id, FilterSet.filter_set_name) \
                .filter(or_(FilterSet.username==username, FilterSet.username=="")) \
                .filter(FilterSet.survey_filter_set=='Y') \
                .all()
    filter_sets = [{"filter_set_id": result[0], "filter_set_name": result[1]} for result in results]
    db.session.close()
    db.engine.dispose()
    return Response(json.dumps(filter_sets), mimetype = 'application/json')

def get_survey_filters(filter_set_id):
    filter_set = db.session.query(FilterSet).filter_by(filter_set_id=filter_set_id).first()
    db.session.close()
    db.engine.dispose()
    return Response(json.dumps(filter_set.to_dict()), mimetype='application/json')

def save_survey_filters(data):
    filter_set = FilterSet(
        filter_set_name=data["filter_set_name"],
        username=data["username"],
        survey_filter_set=data["survey_filter_set"],
        filter_data=data["filter_data"]
    )

    db.session.add(filter_set)
    db.session.commit()
    db.session.close()
    db.engine.dispose()
    # print(filter_set.filter_data)
    return {"message": "successfully saved filter set"}

def delete_survey_filters(filter_set_id):
    db.session.query(FilterSet).filter_by(filter_set_id=filter_set_id).delete()
    db.session.commit()
    db.session.close()
    db.engine.dispose()
    return 'Successfully deleted filter set'