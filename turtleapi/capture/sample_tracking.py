from turtleapi import db
from turtleapi.models.turtlemodels import Sample, SampleTracking
from sqlalchemy.orm import load_only, defer

def add_tracking_entry(data):
    sample = Sample.query.filter_by(sample_id=data['sample_id']).first()

    entry = SampleTracking(
        sample=sample,
        date=data['date'],
        notes=data['notes']
    )
    db.session.add(entry)
    db.session.commit()
    return 'Successfully added tracking entry'

def update_tracking_entry(sample_tracking_id, data):
    entry = SampleTracking.query.filter_by(sample_tracking_id=sample_tracking_id).first()
    entry.date = data['date']
    entry.notes = data['notes']
    db.session.commit()
    return 'Successfully updated tracking entry'

def get_sample(sample_id):
    query_result = db.session.query(Sample).filter_by(sample_id=sample_id).first()
    return query_result.to_dict(max_nesting=1)

def delete_tracking_entry(sample_tracking_id):
    print(sample_tracking_id)
    SampleTracking.query.filter_by(sample_tracking_id=sample_tracking_id).delete()
    db.session.commit()
    return 'Successfully deleted tracking entry'